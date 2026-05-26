#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Level 1 Benchmark测试器 - 统一版本（支持zero-shot和few-shot）
调用API测试benchmark数据集，使用无窗口MATLAB验证，直接运行LLM生成的完整代码，验证results.f的正确性
"""

import os
import json
import argparse
import re
import tempfile
from typing import List, Dict, Any, Tuple, Optional
import time
import requests

# ========== JSON处理 ==========
try:
    import orjson
    def loads(s): return orjson.loads(s)
    def dumps(o): return orjson.dumps(o).decode("utf-8")
except Exception:
    def loads(s): return json.loads(s)
    def dumps(o): return json.dumps(o, ensure_ascii=False)

class Level1_BenchmarkTester:
    """
    Level 1 Benchmark测试器（支持zero-shot和few-shot）
    """
    
    def __init__(
        self,
        api_key: str = None,
        base_url: str = "https://api.deepseek.com/v1",
        model_name: str = "deepseek-chat",
        matlab_timeout: int = 60,
        epsilon: float = 1e-10,
        tolerance: float = 1e-4,
        verbose: bool = True,
        debug: bool = False,
        is_thinking_model: bool = False,
        use_local_model: bool = False,
        local_model_path: str = None
    ):
        """
        初始化测试器
        
        Args:
            api_key: API密钥（使用API时需要）
            base_url: API基础URL
            model_name: 模型名称
            matlab_timeout: MATLAB执行超时时间（秒）
            epsilon: 除法保护的小常数
            tolerance: 允许的相对误差阈值
            verbose: 是否打印详细信息
            debug: 是否启用调试模式（输出API原始响应）
            is_thinking_model: 是否为思考型模型（会使用更长超时和更多tokens）
            use_local_model: 是否使用本地模型
            local_model_path: 本地模型路径
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/') if base_url else ""
        self.model_name = model_name
        self.matlab_timeout = matlab_timeout
        self.epsilon = epsilon
        self.tolerance = tolerance
        self.verbose = verbose
        self.debug = debug
        self.is_thinking_model = is_thinking_model
        self.matlab_engine = None
        
        # 本地模型相关
        self.use_local_model = use_local_model
        self.local_model_path = local_model_path
        self.local_model = None
        self.local_tokenizer = None
        
        # 根据模型类型设置超时和token参数
        if is_thinking_model:
            self.api_timeout = 360  # 思考模型：6分钟
            self.max_tokens = 8000  # 思考模型：8k tokens
        else:
            self.api_timeout = 180  # 非思考模型：3分钟
            self.max_tokens = 4000  # 非思考模型：4k tokens
        
        # 如果使用本地模型，加载模型
        if self.use_local_model:
            self.load_local_model()
        
        # 统计信息
        self.stats = {
            "total": 0,
            "correct": 0,
            "incorrect": 0,
            "error_details": []
        }
    
    def load_local_model(self):
        """加载本地模型"""
        if not self.local_model_path:
            print("❌ 错误: 未指定本地模型路径")
            return False
        
        if self.verbose:
            print(f"🚀 正在加载本地模型: {self.local_model_path}")
        
        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForCausalLM
            
            # 检查模型路径是否存在
            if not os.path.exists(self.local_model_path):
                print(f"❌ 错误: 模型路径不存在: {self.local_model_path}")
                return False
            
            # 加载tokenizer
            self.local_tokenizer = AutoTokenizer.from_pretrained(
                self.local_model_path,
                trust_remote_code=True
            )
            
            # 加载模型
            self.local_model = AutoModelForCausalLM.from_pretrained(
                self.local_model_path,
                torch_dtype=torch.bfloat16,
                device_map="auto",
                trust_remote_code=True
            )
            
            if self.verbose:
                print("✅ 本地模型加载成功")
            
            return True
            
        except ImportError as e:
            print(f"❌ 错误: 缺少依赖库 - {e}")
            print("   请安装: pip install torch transformers accelerate")
            return False
        except Exception as e:
            print(f"❌ 本地模型加载失败: {e}")
            return False
    
    def start_matlab(self):
        """启动MATLAB引擎"""
        if self.verbose:
            print("🚀 正在启动MATLAB引擎（无窗口模式）...")
        
        try:
            import matlab.engine
            # 启动MATLAB引擎，-nodesktop表示无窗口
            self.matlab_engine = matlab.engine.start_matlab("-nodesktop -nosplash")
            
            if self.verbose:
                print("✅ MATLAB引擎启动成功")
            
            return True
            
        except ImportError:
            print("❌ 错误: 未安装 matlab.engine")
            print("   请先安装MATLAB Python引擎:")
            print("   Linux/Mac: cd <MATLAB安装路径>/extern/engines/python && python setup.py install")
            print("   Windows: cd <MATLAB安装路径>\\extern\\engines\\python && python setup.py install")
            print("   示例路径:")
            print("     - Mac: /Applications/MATLAB_R20XXx.app/extern/engines/python")
            print("     - Linux: /usr/local/MATLAB/R20XXx/extern/engines/python")
            print("     - Windows: C:\\Program Files\\MATLAB\\R20XXx\\extern\\engines\\python")
            return False
        except Exception as e:
            print(f"❌ MATLAB引擎启动失败: {e}")
            return False
    
    def stop_matlab(self):
        """停止MATLAB引擎"""
        if self.matlab_engine:
            if self.verbose:
                print("🛑 正在关闭MATLAB引擎...")
            self.matlab_engine.quit()
            self.matlab_engine = None
    
    def call_local_model(self, prompt: str) -> tuple[Optional[str], Optional[str]]:
        """
        调用本地模型生成代码
        
        Args:
            prompt: 提示词
            
        Returns:
            (模型返回的文本, finish_reason)，失败返回(None, None)
        """
        if not self.local_model or not self.local_tokenizer:
            if self.verbose:
                print("❌ 本地模型未加载")
            return None, None
        
        try:
            import torch
            
            # 构建消息
            messages = [
                {
                    "role": "system",
                    "content": "You are an expert in MATPOWER and power systems optimization. Generate MATLAB code following the instructions precisely."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            # 应用聊天模板
            text = self.local_tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            
            # 编码输入
            model_inputs = self.local_tokenizer([text], return_tensors="pt").to(self.local_model.device)
            
            # 生成输出
            with torch.no_grad():
                generated_ids = self.local_model.generate(
                    **model_inputs,
                    max_new_tokens=self.max_tokens,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=self.local_tokenizer.eos_token_id
                )
            
            # 解码输出（只取新生成的部分）
            generated_ids = [
                output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
            ]
            
            response = self.local_tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
            
            # 判断是否因为长度而停止
            finish_reason = 'length' if len(generated_ids[0]) >= self.max_tokens else 'stop'
            
            return response, finish_reason
            
        except Exception as e:
            if self.verbose:
                print(f"❌ 本地模型推理失败: {e}")
            return None, None
    
    def call_llm_api(self, prompt: str, max_retries: int = 3) -> tuple[Optional[str], Optional[str]]:
        """
        调用LLM API生成代码（失败后最多重试max_retries次）
        支持流式响应以处理思考型模型
        
        Args:
            prompt: 提示词
            max_retries: 最大重试次数（默认3次）
            
        Returns:
            (API返回的文本, finish_reason)，失败返回(None, None)
            finish_reason可能的值: 'stop'(正常结束), 'length'(token超限), None(其他)
        """
        # 如果使用本地模型，直接调用本地模型
        if self.use_local_model:
            return self.call_local_model(prompt)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": self.model_name,
            "messages": [
                {
                    "role": "system",
                    "content": "You are an expert in MATPOWER and power systems optimization. Generate MATLAB code following the instructions precisely."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.7,
            "max_tokens": self.max_tokens,
            "stream": True  # 启用流式响应
        }
        
        for attempt in range(1, max_retries + 1):
            try:
                if self.verbose and attempt > 1:
                    print(f"  🔄 重试第 {attempt-1} 次...")
                
                response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=self.api_timeout,
                    stream=True   # 启用流式响应
                )
                
                if response.status_code == 200:
                    # 收集流式响应
                    full_content = ""
                    reasoning_content = ""  # 单独收集reasoning_content用于调试
                    chunk_count = 0
                    all_chunks = []  # 保存所有chunk用于调试
                    finish_reason = None  # 记录结束原因
                    
                    for line in response.iter_lines():
                        if line:
                            line_text = line.decode('utf-8')
                            
                            # 跳过空行和事件名
                            if not line_text.strip() or line_text.startswith(':'):
                                continue
                            
                            # 移除 "data: " 前缀
                            if line_text.startswith('data: '):
                                line_text = line_text[6:]
                            
                            # 检查是否是结束标记
                            if line_text.strip() == '[DONE]':
                                break
                            
                            try:
                                chunk = json.loads(line_text)
                                chunk_count += 1
                                all_chunks.append(chunk)  # 保存chunk
                                
                                # 调试模式：打印原始chunk
                                if self.debug and chunk_count <= 5:
                                    print(f"  [DEBUG] Chunk {chunk_count}: {json.dumps(chunk, ensure_ascii=False)[:500]}")
                                    # 显示delta的完整结构
                                    if 'choices' in chunk and len(chunk['choices']) > 0:
                                        delta = chunk['choices'][0].get('delta', {})
                                        print(f"  [DEBUG] Delta keys: {list(delta.keys())}")
                                
                                # 提取内容 - 支持多种格式
                                if 'choices' in chunk and len(chunk['choices']) > 0:
                                    choice = chunk['choices'][0]
                                    
                                    # 检查finish_reason以判断是否因为token超出而结束
                                    if 'finish_reason' in choice and choice['finish_reason']:
                                        finish_reason = choice['finish_reason']
                                    
                                    # 尝试从delta中获取（流式响应）
                                    delta = choice.get('delta', {})
                                    content = delta.get('content', '')
                                    
                                    # 单独收集reasoning_content用于调试（不用于最终结果）
                                    reasoning = delta.get('reasoning_content', '')
                                    if reasoning:
                                        reasoning_content += reasoning
                                    
                                    # 如果delta中没有content，尝试从message中获取（某些思考型模型）
                                    if not content and 'message' in choice:
                                        content = choice['message'].get('content', '')
                                    
                                    # 如果还是没有，尝试直接从choice获取text字段（某些API格式）
                                    if not content:
                                        content = choice.get('text', '')
                                    
                                    if content:
                                        full_content += content
                                        if self.debug:
                                            print(f"  [DEBUG] 提取到内容: {content[:50]}...")
                            
                            except json.JSONDecodeError as e:
                                # 跳过无法解析的行
                                if self.verbose and attempt == 1:
                                    print(f"  ⚠️  JSON解析失败: {str(e)[:100]}")
                                continue
                    
                    if full_content:
                        # 检查是否因为token超出而结束
                        if finish_reason == 'length':
                            if self.verbose:
                                print(f"  ⚠️  警告: API响应因达到最大token限制而截断 (finish_reason=length)")
                                print(f"  ⚠️  该响应将被标记为incorrect并保存")
                        
                        if self.verbose and attempt > 1:
                            print(f"  ✅ 成功获取响应 (共 {chunk_count} 个数据块)")
                        return full_content, finish_reason
                    else:
                        if self.verbose:
                            print(f"  ❌ API返回内容为空 (尝试 {attempt}/{max_retries}, 收到 {chunk_count} 个数据块)")
                            # 打印已经收到的content（如果有的话）
                            if full_content:
                                print(f"  📄 已收到的content: {full_content[:500]}...")
                            else:
                                print(f"  📄 已收到的content: (无)")
                            
                            # 打印reasoning_content用于调试（不用于最终结果）
                            if reasoning_content:
                                print(f"  🧠 收到的reasoning_content (仅用于调试):")
                                print(f"      {reasoning_content[:500]}...")
                                if len(reasoning_content) > 500:
                                    print(f"      ... (共 {len(reasoning_content)} 字符)")
                            
                            # 打印前几个chunk的结构用于调试
                            if all_chunks and self.verbose:
                                print(f"  🔍 前3个数据块的结构:")
                                for i, chunk in enumerate(all_chunks[:3], 1):
                                    print(f"      Chunk {i}: {json.dumps(chunk, ensure_ascii=False)[:300]}")
                else:
                    if self.verbose:
                        print(f"  ❌ API请求失败 (状态码: {response.status_code}, 尝试 {attempt}/{max_retries})")
                        # 打印错误响应体以便调试
                        try:
                            error_body = response.text[:500] if hasattr(response, 'text') else str(response.content[:500])
                            print(f"  📄 错误响应: {error_body}")
                        except:
                            pass
                    
            except requests.exceptions.Timeout:
                if self.verbose:
                    print(f"  ❌ API调用超时（超过{self.api_timeout}秒, 尝试 {attempt}/{max_retries}）")
            except Exception as e:
                if self.verbose:
                    print(f"  ❌ API调用异常: {e} (尝试 {attempt}/{max_retries})")
            
            # 如果不是最后一次尝试，等待一下再重试
            if attempt < max_retries:
                time.sleep(2)
        
        # 所有尝试都失败
        if self.verbose:
            print(f"  ❌ API调用失败，已重试 {max_retries} 次")
        return None, None
    
    def extract_matlab_code(self, llm_output: str) -> Optional[str]:
        """
        从LLM输出中提取MATLAB代码
        
        Args:
            llm_output: LLM的输出文本
            
        Returns:
            提取的MATLAB代码，失败返回None
        """
        # 尝试提取代码块中的内容
        patterns = [
            r'```matlab\s*(.*?)\s*```',
            r'```\s*(define_constants;.*?printpf\(results\);)\s*```',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, llm_output, re.DOTALL | re.IGNORECASE)
            if matches:
                code = matches[0].strip()
                # 验证是否包含必要的MATPOWER元素
                if 'loadcase' in code and 'runopf' in code:
                    return code
        
        # 如果没有代码块，尝试直接查找从define_constants开始到printpf结束的代码
        if 'define_constants' in llm_output and 'runopf' in llm_output:
            # 查找从define_constants开始的代码
            start_idx = llm_output.find('define_constants')
            if start_idx >= 0:
                # 查找printpf(results)
                end_pattern = r'printpf\(results\);'
                end_match = re.search(end_pattern, llm_output[start_idx:])
                if end_match:
                    end_idx = start_idx + end_match.end()
                    code = llm_output[start_idx:end_idx].strip()
                    return code
        
        return None
    
    def build_prompt(self, sample: Dict[str, Any], few_shot_examples: List[Dict[str, Any]] = None) -> str:
        """
        构建LLM提示词（支持few-shot learning）
        
        Args:
            sample: 当前要处理的样本数据
            few_shot_examples: few-shot示例列表，每个示例包含natural_language和matpower_code（None表示zero-shot）
            
        Returns:
            提示词字符串
        """
        nl_description = sample.get("natural_language", "")
        
        # 构建few-shot示例部分（如果有示例）
        few_shot_section = ""
        if few_shot_examples:
            few_shot_section = "\n**Few-shot Examples:**\n\n"
            for i, example in enumerate(few_shot_examples, 1):
                ex_nl = example.get("natural_language", "")
                ex_code = example.get("matpower_code", "")
                few_shot_section += f"Example {i}:\n"
                few_shot_section += f"Description: {ex_nl}\n\n"
                few_shot_section += f"MATLAB Code:\n```matlab\n{ex_code}\n```\n\n"
            few_shot_section += "---\n\n"
        
        # 根据是否有few-shot示例调整prompt格式
        if few_shot_examples:
            task_label = "**Current Task:**"
        else:
            task_label = ""
        
        prompt = f"""You are an expert in MATPOWER and power systems optimization.

Based on the following natural language description, generate a complete, executable MATLAB script that implements the described optimal power flow analysis.

{few_shot_section}{task_label}
Description:
{nl_description}

**Requirements:**
1. Generate a complete MATLAB script that can be executed directly
2. Start with `define_constants;` to load MATPOWER constants
3. Load the appropriate case file using `loadcase()`
4. Apply all parameter modifications as described
5. **Configure the solver options as specified. If modifications are needed, use "opf.violation"**
6. Run the optimal power flow using `runopf(mpc, mpopt)`
7. End with `printpf(results);` to display results
8. The code should be ready to run without any modifications

Output the complete MATLAB script directly, without any explanations or additional text.
"""
        
        return prompt
    
    def run_matlab_code(
        self,
        matlab_code: str,
        sample_id: int
    ) -> Tuple[str, Optional[float], str]:
        """
        在MATLAB中运行完整代码并获取results.f
        
        Args:
            matlab_code: 完整的MATLAB代码
            sample_id: 样本ID
            
        Returns:
            (状态, f值, 错误信息)
            状态: "success" - 成功执行
                  "error" - 执行出错
        """
        if not self.matlab_engine:
            return "error", None, "MATLAB引擎未启动"
        
        temp_file = None
        try:
            # 创建临时.m文件
            with tempfile.NamedTemporaryFile(mode='w', suffix='.m', delete=False, encoding='utf-8') as f:
                temp_file = f.name
                f.write(matlab_code)
            
            # 获取临时文件的目录和文件名（不含.m扩展名）
            temp_dir = os.path.dirname(temp_file)
            temp_name = os.path.splitext(os.path.basename(temp_file))[0]
            
            # 将临时目录添加到MATLAB路径
            self.matlab_engine.addpath(temp_dir, nargout=0)
            
            # 运行临时脚本
            self.matlab_engine.eval(temp_name, nargout=0)
            
            # 获取results.f的值
            f_value = self.matlab_engine.eval("results.f", nargout=1)
            
            if self.verbose:
                print(f"  ✅ 样本 {sample_id}: MATLAB执行成功 (f={f_value:.6f})")
            
            return "success", float(f_value), ""
            
        except Exception as e:
            error_msg = str(e)
            if self.verbose:
                print(f"  ❌ 样本 {sample_id}: MATLAB执行失败")
                print(f"     错误: {error_msg[:200]}...")
            
            return "error", None, error_msg
            
        finally:
            # 清理临时文件
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
    
    def check_correctness(self, output: float, ground_truth: float) -> bool:
        """
        根据公式检查输出是否正确: |o - g| / |g + ε| <= tolerance
        
        Args:
            output: 输出值
            ground_truth: 真实值
            
        Returns:
            是否正确
        """
        numerator = abs(output - ground_truth)
        denominator = abs(ground_truth + self.epsilon)
        relative_error = numerator / denominator
        
        return relative_error <= self.tolerance
    
    def test_sample(
        self,
        sample: Dict[str, Any],
        sample_id: int,
        few_shot_examples: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        测试单个样本
        
        Args:
            sample: 样本数据
            sample_id: 样本ID
            few_shot_examples: few-shot示例列表（可选，None表示zero-shot）
            
        Returns:
            测试结果
        """
        # 提取正确答案
        ground_truth = sample.get("results", {}).get("objective_value")
        
        result = {
            "sample_id": sample_id,
            "status": "incorrect",  # 默认为不正确
            "natural_language": sample.get("natural_language", ""),
            "ground_truth": ground_truth,
            "model_output": None,
            "llm_raw_output": None,  # 新增字段：LLM原始输出
            "complete_matlab_code": None,  # 新增字段：完整可执行代码
            "error": None,
            "is_api_error": False,  # 标记是否是API错误（用于判断是否终止测试）
            "token_limit_exceeded": False  # 标记是否超过token限制
        }
        
        # 1. 构建提示词（传入few-shot示例，如果为None则使用zero-shot）
        prompt = self.build_prompt(sample, few_shot_examples)
        
        # 2. 调用LLM API 或 本地模型
        if self.verbose:
            if self.use_local_model:
                print(f"\n📝 样本 {sample_id}: 调用本地模型...")
            else:
                print(f"\n📝 样本 {sample_id}: 调用LLM API...")
        
        llm_output, finish_reason = self.call_llm_api(prompt, max_retries=3)
        if llm_output is None:
            result["error"] = "API调用失败（已重试3次）"
            result["is_api_error"] = True  # 标记为API错误
            self.stats["incorrect"] += 1
            return result
        
        # 检查是否因为token超限
        if finish_reason == 'length':
            result["token_limit_exceeded"] = True
            result["error"] = "响应因达到最大token限制而截断"
            result["status"] = "incorrect"
        
        # 保存LLM原始输出
        result["llm_raw_output"] = llm_output
        
        # 3. 提取MATLAB代码
        if self.verbose:
            print(f"  🔍 样本 {sample_id}: 提取MATLAB代码...")
        
        matlab_code = self.extract_matlab_code(llm_output)
        if matlab_code is None:
            if not result["token_limit_exceeded"]:
                result["error"] = "无法提取MATLAB代码"
            else:
                result["error"] = "响应因达到最大token限制而截断，且无法提取MATLAB代码"
            result["is_api_error"] = False  # 不是API错误，不终止测试
            self.stats["incorrect"] += 1
            return result
        
        # 保存提取的代码
        result["complete_matlab_code"] = matlab_code
        
        # 4. 运行MATLAB代码
        if ground_truth is not None:
            status, f_value, error = self.run_matlab_code(matlab_code, sample_id)
            
            if status == "success" and f_value is not None:
                result["model_output"] = f_value
                is_correct = self.check_correctness(f_value, ground_truth)
                result["status"] = "correct" if is_correct else "incorrect"
                
                if is_correct:
                    self.stats["correct"] += 1
                else:
                    self.stats["incorrect"] += 1
            else:
                # MATLAB执行失败，不是API错误，不终止测试
                result["status"] = "incorrect"
                result["error"] = error
                result["is_api_error"] = False
                self.stats["incorrect"] += 1
        
        return result
    
    def load_few_shot_examples(self, example_file: str, num_examples: int = 3) -> List[Dict[str, Any]]:
        """
        从示例文件加载few-shot示例
        
        Args:
            example_file: 示例文件路径
            num_examples: 要加载的示例数量（默认3个）
            
        Returns:
            few-shot示例列表
        """
        few_shot_examples = []
        if not example_file or not os.path.exists(example_file):
            if self.verbose:
                print(f"  ⚠️  示例文件不存在: {example_file}，将使用zero-shot模式")
            return few_shot_examples
        
        try:
            with open(example_file, 'r', encoding='utf-8') as f:
                for line in f:
                    if len(few_shot_examples) >= num_examples:
                        break
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        example = loads(line)
                        # 确保示例包含必要的字段
                        if example.get("natural_language") and example.get("matpower_code"):
                            few_shot_examples.append(example)
                    except:
                        continue
        except Exception as e:
            if self.verbose:
                print(f"  ⚠️  加载few-shot示例失败: {e}，将使用zero-shot模式")
        
        return few_shot_examples
    
    def test_benchmark(
        self,
        input_file: str,
        output_file: str,
        start_index: Optional[int] = None,
        end_index: Optional[int] = None,
        example_file: Optional[str] = None,
        use_few_shot: bool = False
    ) -> Dict[str, int]:
        """
        测试整个benchmark数据集
        
        Args:
            input_file: 输入JSONL文件路径
            output_file: 结果输出路径
            start_index: 起始样本编号（从1开始，None表示从头开始）
            end_index: 结束样本编号（包含，None表示到末尾）
            example_file: few-shot示例文件路径（仅在use_few_shot=True时使用）
            use_few_shot: 是否使用few-shot模式
            
        Returns:
            统计信息字典
        """
        # 重置统计
        self.stats = {
            "total": 0,
            "correct": 0,
            "incorrect": 0,
            "error_details": []
        }
        
        # 检查文件是否存在
        if not os.path.exists(input_file):
            print(f"❌ 错误: 文件不存在 {input_file}")
            return self.stats
        
        # 启动MATLAB
        if not self.start_matlab():
            return self.stats
        
        # 创建输出目录
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        # 读取数据
        if self.verbose:
            print(f"\n📖 读取benchmark数据集: {input_file}")
            if start_index is not None or end_index is not None:
                range_str = f"处理范围: 样本 {start_index or 1} 到 {end_index or '末尾'}"
                print(f"  {range_str}")
        
        # 加载few-shot示例（仅在use_few_shot=True时加载）
        few_shot_examples = None
        if use_few_shot:
            few_shot_examples = self.load_few_shot_examples(example_file, num_examples=3)
            if self.verbose:
                if few_shot_examples:
                    print(f"  📚 已从示例文件加载 {len(few_shot_examples)} 个few-shot示例")
                else:
                    print(f"  📚 未加载few-shot示例，将使用zero-shot模式")
        else:
            if self.verbose:
                print(f"  📚 使用zero-shot模式（未启用few-shot）")
        
        # 打开输出文件（追加模式）
        with open(output_file, 'a', encoding='utf-8') as out_f:
            with open(input_file, 'r', encoding='utf-8') as in_f:
                for line_num, line in enumerate(in_f, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    # 检查是否在指定范围内
                    if start_index is not None and line_num < start_index:
                        continue
                    if end_index is not None and line_num > end_index:
                        break
                    
                    self.stats["total"] += 1
                    
                    try:
                        # 解析JSON
                        sample = loads(line)
                        
                        # 测试样本（传入few-shot示例，如果为None则使用zero-shot）
                        result = self.test_sample(sample, line_num, few_shot_examples)
                        
                        # 检查是否是API错误
                        if result.get("is_api_error"):
                            # 仅API错误时终止测试（不保存该条数据）
                            error_msg = result["error"]
                            self.stats["error_details"].append({
                                "line": line_num,
                                "error": error_msg[:200]
                            })
                            
                            if self.verbose:
                                print(f"\n❌ API调用失败（已重试3次），立即终止测试！")
                                print(f"   错误位置: 样本 {line_num}")
                                print(f"   错误信息: {error_msg[:200]}")
                                print(f"   该条数据不会保存到文件")
                            
                            # 关闭MATLAB
                            self.stop_matlab()
                            
                            # 立即终止测试（不保存错误的数据）
                            return self.stats
                        
                        # 保存所有结果（包括正确的和非API错误的）
                        # 移除内部字段 is_api_error，不保存到输出文件
                        output_result = {k: v for k, v in result.items() if k != "is_api_error"}
                        out_f.write(dumps(output_result) + "\n")
                        out_f.flush()  # 立即写入磁盘
                        
                        # 如果token超限，在控制台显示提示
                        if result.get("token_limit_exceeded"):
                            if self.verbose:
                                print(f"  ⚠️  样本 {line_num}: Token超限，已保存为incorrect")
                        
                    except json.JSONDecodeError as e:
                        if self.verbose:
                            print(f"  ❌ 样本 {line_num}: JSON解析失败 - {e}")
                            print(f"     终止测试！")
                        self.stop_matlab()
                        return self.stats
                    
                    except Exception as e:
                        if self.verbose:
                            print(f"  ❌ 样本 {line_num}: 未知错误 - {e}")
                            print(f"     终止测试！")
                        self.stop_matlab()
                        return self.stats
        
        # 关闭MATLAB
        self.stop_matlab()
        
        if self.verbose:
            print(f"\n💾 所有结果已实时保存到: {output_file}")
        
        return self.stats
    
    def print_stats(self):
        """打印统计信息"""
        print(f"\n{'='*60}")
        print(f"📊 测试统计")
        print(f"{'='*60}")
        print(f"总样本数:              {self.stats['total']}")
        print(f"✅ 正确:               {self.stats['correct']} ({self.stats['correct']/max(self.stats['total'],1)*100:.1f}%)")
        print(f"❌ 错误:               {self.stats['incorrect']} ({self.stats['incorrect']/max(self.stats['total'],1)*100:.1f}%)")
        
        if self.stats['error_details'] and self.verbose:
            print(f"\n错误详情:")
            for i, err in enumerate(self.stats['error_details'], 1):
                print(f"  {i}. 样本 {err['line']}: {err['error'][:100]}...")
        
        print(f"{'='*60}")


# ========== 命令行入口 ==========
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""Level 1 Benchmark测试器 - 统一版本（支持zero-shot和few-shot）
        
错误处理策略:
  - API调用失败: 自动重试最多3次，3次都失败后终止测试（不保存失败数据）
  - 其他错误(代码提取失败、MATLAB执行失败、结果不匹配): 继续测试并保存错误数据
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  # Zero-shot模式测试（默认）
  python LLM_test/test_level1.py --output base_test_output/level1_test_{model}_output.jsonl --model deepseek-chat
  
  # Few-shot模式测试
  python LLM_test/test_level1.py --output base_test_output/level1_test_{model}_output.jsonl --model deepseek-chat --few-shot --example-file ProOPF_D/level1_data_example.jsonl
  
  # 指定输入文件和API配置
  python LLM_test/test_level1.py --output level1_test.jsonl --model deepseek-chat --input-file ProOPF_B/level1_with_labels.jsonl --api-key YOUR_API_KEY --base-url https://api.deepseek.com/v1
  
  # 指定处理范围（处理第1到第10个样本）
  python LLM_test/test_level1.py --output level1_test.jsonl --model deepseek-chat --start 1 --end 10
  
  # 使用本地模型测试
  python LLM_test/test_level1.py --output local_test.jsonl --local-model /path/to/model
        """
    )
    
    parser.add_argument("--output", type=str, required=True,
                       help="输出文件名（将保存到results/level1目录下）")
    parser.add_argument("--model", type=str, default="deepseek-chat",
                       help="模型名称 (默认: deepseek-chat)")
    parser.add_argument("--input-file", type=str, default=None,
                       help="输入文件路径（默认: ProOPF_B/level1_with_labels.jsonl）")
    parser.add_argument("--few-shot", action="store_true",
                       help="启用few-shot模式（默认: zero-shot模式）")
    parser.add_argument("--example-file", type=str, default=None,
                       help="Few-shot示例文件路径（仅在--few-shot时使用，默认: ProOPF_D/level1_data_example.jsonl）")
    parser.add_argument("--api-key", type=str, default=None,
                       help="API密钥（默认: 从环境变量LLM_API_KEY获取，或使用DeepSeek默认值）")
    parser.add_argument("--base-url", type=str, default=None,
                       help="API基础URL（默认: 从环境变量LLM_BASE_URL获取，或使用DeepSeek默认值）")
    parser.add_argument("--start", type=int, default=None,
                       help="起始样本编号（从1开始，不指定则从头开始）")
    parser.add_argument("--end", type=int, default=None,
                       help="结束样本编号（包含，不指定则到末尾）")
    parser.add_argument("--debug", action="store_true",
                       help="启用调试模式（输出API原始响应数据）")
    parser.add_argument("--thinking", action="store_true",
                       help="使用思考型模型（启用更长超时时间和更多tokens）")
    parser.add_argument("--local-model", type=str, default=None,
                       help="本地模型路径（指定后将使用本地模型而非API）")
    
    args = parser.parse_args()
    
    # 配置处理：优先使用命令行参数，其次环境变量，最后使用默认值
    input_file = args.input_file if args.input_file else "ProOPF_B/level1_with_labels.jsonl"
    
    # 如果启用few-shot，设置示例文件路径
    example_file = None
    if args.few_shot:
        example_file = args.example_file if args.example_file else "ProOPF_D/level1_data_example.jsonl"
    
    # API密钥：命令行参数 > 环境变量 > 默认值
    if args.api_key:
        api_key = args.api_key
    else:
        api_key = os.environ.get("LLM_API_KEY", "sk-8803a580773749828785964c20e5fdb8")
    
    # API URL：命令行参数 > 环境变量 > 默认值
    if args.base_url:
        base_url = args.base_url
    else:
        base_url = os.environ.get("LLM_BASE_URL", "https://api.deepseek.com/v1")
    
    # 判断是否使用本地模型
    use_local = args.local_model is not None
    
    # 确定实际使用的模型名（用于文件名替换）
    actual_model_name = args.local_model if use_local else args.model
    # 清理模型名中的特殊字符，用于文件名
    safe_model_name = actual_model_name.replace("/", "_").replace("\\", "_").replace(":", "_")
    
    # 输出文件路径（如果输出路径包含目录，则使用该目录；否则放到results/level1目录下）
    # 支持 {model} 占位符，自动替换为实际模型名
    output_template = args.output
    if "{model}" in output_template:
        output_template = output_template.replace("{model}", safe_model_name)
    
    if os.path.dirname(output_template):
        # 如果输出参数包含目录路径，直接使用
        output_file = output_template
    else:
        # 否则放到默认目录
        output_file = os.path.join("../results/level1", output_template)
    
    # 创建测试器
    tester = Level1_BenchmarkTester(
        api_key=api_key if not use_local else None,
        base_url=base_url if not use_local else None,
        model_name=args.model,
        matlab_timeout=60,
        tolerance=1e-4,
        verbose=True,
        debug=args.debug,
        is_thinking_model=args.thinking,
        use_local_model=use_local,
        local_model_path=args.local_model
    )
    
    # 测试benchmark
    print(f"{'='*60}")
    print(f"🧪 Level 1 Benchmark测试器 ({'Few-shot' if args.few_shot else 'Zero-shot'}模式)")
    print(f"{'='*60}")
    print(f"输入文件:     {input_file}")
    print(f"输出文件:     {output_file}")
    
    if use_local:
        print(f"推理方式:     本地模型")
        print(f"模型路径:     {args.local_model}")
    else:
        print(f"推理方式:     远程API")
        print(f"API URL:      {base_url}")
        print(f"模型:         {args.model}")
    
    print(f"模式:         {'Few-shot' if args.few_shot else 'Zero-shot'}")
    if args.few_shot:
        print(f"示例文件:     {example_file}")
    print(f"模型类型:     {'思考型模型' if args.thinking else '标准模型'}")
    if not use_local:
        print(f"API超时:      {tester.api_timeout}秒")
    print(f"Max Tokens:   {tester.max_tokens}")
    print(f"容忍度:       1e-4")
    
    # 显示处理范围
    if args.start is not None or args.end is not None:
        range_str = f"样本 {args.start or 1} 到 {args.end or '末尾'}"
        print(f"处理范围:     {range_str}")
    else:
        print(f"处理范围:     所有样本")
    
    print(f"保存模式:     实时保存（每条立即写入）")
    if use_local:
        print(f"错误处理:     模型推理失败后继续测试；其他错误继续测试")
    else:
        print(f"错误处理:     API失败自动重试3次，3次都失败后终止；其他错误继续测试")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    stats = tester.test_benchmark(
        input_file=input_file,
        output_file=output_file,
        start_index=args.start,
        end_index=args.end,
        example_file=example_file,
        use_few_shot=args.few_shot
    )
    
    elapsed_time = time.time() - start_time
    
    # 打印统计
    tester.print_stats()
    print(f"\n⏱️  总耗时: {elapsed_time:.1f} 秒")
    print(f"✨ 完成！测试结果保存到: {output_file}\n")

