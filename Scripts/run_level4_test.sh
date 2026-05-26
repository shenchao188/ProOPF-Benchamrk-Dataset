#!/bin/bash
# Level 4 Benchmark测试脚本 - 支持zero-shot和few-shot模式
# 用法: ./run_level4_test.sh [选项]
#
# 重要提示：
#   1. 请在使用前配置以下参数：
#      - MODEL: 您要使用的模型名称（如：deepseek-chat, gpt-4, claude-3等）
#      - API_KEY: 您的API密钥（可通过环境变量LLM_API_KEY设置，或通过--api-key参数传入）
#      - BASE_URL: API的基础URL（可通过环境变量LLM_BASE_URL设置，或通过--base-url参数传入）
#   2. 您可以通过以下方式配置：
#      - 方式1: 设置环境变量（推荐）
#        export LLM_API_KEY="your-api-key-here"
#        export LLM_BASE_URL="https://api.example.com/v1"
#      - 方式2: 通过命令行参数传入
#        ./run_level4_test.sh --api-key YOUR_KEY --base-url https://api.example.com/v1 --model MODEL_NAME

# 默认配置
MODEL="${LLM_MODEL_NAME:-YOUR_MODEL_NAME}"  # 请替换为您的模型名称，或通过--model参数传入
INPUT_FILE="ProOPF_B/level4_with_labels.jsonl"
EXAMPLE_FILE="ProOPF_D/level4_data_example.jsonl"
OUTPUT_DIR="base_test_output"
API_KEY="${LLM_API_KEY:-YOUR_API_KEY_HERE}"  # 请替换为您的API密钥，或通过环境变量LLM_API_KEY设置
BASE_URL="${LLM_BASE_URL:-YOUR_API_BASE_URL_HERE}"  # 请替换为您的API基础URL，或通过环境变量LLM_BASE_URL设置
START_IDX=""
END_IDX=""
DEBUG=""
THINKING=""
LOCAL_MODEL=""

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印帮助信息
print_help() {
    echo "Level 4 Benchmark测试脚本 - 最高难度级别"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --model MODEL           模型名称 (必需，请填入您要使用的模型名称)"
    echo "  --input-file FILE       输入文件路径 (默认: ProOPF_B/level4_with_labels.jsonl)"
    echo "  --example-file FILE     Few-shot示例文件路径 (默认: ProOPF_D/level4_data_example.jsonl)"
    echo "  --output-dir DIR         输出目录 (默认: base_test_output)"
    echo "  --api-key KEY           API密钥 (必需，请填入您的API密钥，或通过环境变量LLM_API_KEY设置)"
    echo "  --base-url URL          API基础URL (必需，请填入您的API基础URL，或通过环境变量LLM_BASE_URL设置)"
    echo "  --start N               起始样本编号"
    echo "  --end N                 结束样本编号"
    echo "  --debug                 启用调试模式"
    echo "  --thinking              使用思考型模型（推荐用于Level 4）"
    echo "  --local-model PATH      本地模型路径"
    echo "  --zero-shot             仅运行zero-shot测试"
    echo "  --few-shot              仅运行few-shot测试"
    echo "  --both                  同时运行zero-shot和few-shot测试（默认）"
    echo "  -h, --help              显示帮助信息"
    echo ""
    echo "示例:"
    echo "  # 同时运行zero-shot和few-shot测试（需要配置API信息）"
    echo "  $0 --model YOUR_MODEL_NAME --api-key YOUR_API_KEY --base-url YOUR_API_BASE_URL"
    echo ""
    echo "  # 仅运行few-shot测试"
    echo "  $0 --few-shot --model YOUR_MODEL_NAME --api-key YOUR_API_KEY --base-url YOUR_API_BASE_URL"
    echo ""
    echo "  # 指定测试范围"
    echo "  $0 --start 1 --end 10 --model YOUR_MODEL_NAME --api-key YOUR_API_KEY --base-url YOUR_API_BASE_URL"
    echo ""
    echo "  # 使用思考型模型（推荐用于Level 4）"
    echo "  $0 --thinking --model YOUR_MODEL_NAME --api-key YOUR_API_KEY --base-url YOUR_API_BASE_URL"
    echo ""
    echo "  # 使用环境变量配置（推荐）"
    echo "  export LLM_API_KEY=\"your-api-key\""
    echo "  export LLM_BASE_URL=\"https://api.example.com/v1\""
    echo "  export LLM_MODEL_NAME=\"your-model-name\""
    echo "  $0"
}

# 解析命令行参数
MODE="both"  # 默认同时运行两种模式

while [[ $# -gt 0 ]]; do
    case $1 in
        --model)
            MODEL="$2"
            shift 2
            ;;
        --input-file)
            INPUT_FILE="$2"
            shift 2
            ;;
        --example-file)
            EXAMPLE_FILE="$2"
            shift 2
            ;;
        --output-dir)
            OUTPUT_DIR="$2"
            shift 2
            ;;
        --api-key)
            API_KEY="$2"
            shift 2
            ;;
        --base-url)
            BASE_URL="$2"
            shift 2
            ;;
        --start)
            START_IDX="--start $2"
            shift 2
            ;;
        --end)
            END_IDX="--end $2"
            shift 2
            ;;
        --debug)
            DEBUG="--debug"
            shift
            ;;
        --thinking)
            THINKING="--thinking"
            shift
            ;;
        --local-model)
            LOCAL_MODEL="--local-model $2"
            shift 2
            ;;
        --zero-shot)
            MODE="zero-shot"
            shift
            ;;
        --few-shot)
            MODE="few-shot"
            shift
            ;;
        --both)
            MODE="both"
            shift
            ;;
        -h|--help)
            print_help
            exit 0
            ;;
        *)
            echo -e "${RED}错误: 未知参数 $1${NC}"
            print_help
            exit 1
            ;;
    esac
done

# 获取脚本所在目录的父目录（项目根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# 清理模型名中的特殊字符，用于文件名
SAFE_MODEL_NAME=$(echo "$MODEL" | sed 's/[\/\\:]/_/g')

# 构建基础命令
BASE_CMD="python LLM_test/test_level4.py"
BASE_CMD="$BASE_CMD --model $MODEL"
BASE_CMD="$BASE_CMD --input-file $INPUT_FILE"
BASE_CMD="$BASE_CMD --api-key $API_KEY"
BASE_CMD="$BASE_CMD --base-url $BASE_URL"

if [ -n "$START_IDX" ]; then
    BASE_CMD="$BASE_CMD $START_IDX"
fi

if [ -n "$END_IDX" ]; then
    BASE_CMD="$BASE_CMD $END_IDX"
fi

if [ -n "$DEBUG" ]; then
    BASE_CMD="$BASE_CMD $DEBUG"
fi

if [ -n "$THINKING" ]; then
    BASE_CMD="$BASE_CMD $THINKING"
fi

if [ -n "$LOCAL_MODEL" ]; then
    BASE_CMD="$BASE_CMD $LOCAL_MODEL"
fi

# 运行测试函数
run_test() {
    local mode=$1
    local output_file="$OUTPUT_DIR/level4_test_${SAFE_MODEL_NAME}_${mode}_output.jsonl"
    
    echo ""
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}运行 ${mode} 测试${NC}"
    echo -e "${BLUE}========================================${NC}"
    echo -e "${GREEN}输出文件: ${output_file}${NC}"
    echo ""
    
    local cmd="$BASE_CMD --output $output_file"
    
    if [ "$mode" = "few-shot" ]; then
        cmd="$cmd --few-shot --example-file $EXAMPLE_FILE"
    fi
    
    echo -e "${YELLOW}执行命令:${NC}"
    echo "$cmd"
    echo ""
    
    # 执行命令
    eval $cmd
    
    local exit_code=$?
    
    if [ $exit_code -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✅ ${mode} 测试完成！${NC}"
        echo -e "${GREEN}结果保存到: ${output_file}${NC}"
    else
        echo ""
        echo -e "${RED}❌ ${mode} 测试失败！退出码: $exit_code${NC}"
        return $exit_code
    fi
    
    return $exit_code
}

# 主执行逻辑
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}Level 4 Benchmark测试脚本${NC}"
echo -e "${BLUE}（最高难度级别 - 推荐使用思考型模型）${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}模型: ${MODEL}${NC}"
echo -e "${GREEN}输入文件: ${INPUT_FILE}${NC}"
if [ "$MODE" = "few-shot" ] || [ "$MODE" = "both" ]; then
    echo -e "${GREEN}示例文件: ${EXAMPLE_FILE}${NC}"
fi
echo -e "${GREEN}输出目录: ${OUTPUT_DIR}${NC}"
echo ""

# 创建输出目录
mkdir -p "$OUTPUT_DIR"

# 根据模式运行测试
EXIT_CODE=0

case $MODE in
    zero-shot)
        run_test "zeroshot"
        EXIT_CODE=$?
        ;;
    few-shot)
        run_test "fewshot"
        EXIT_CODE=$?
        ;;
    both)
        echo -e "${YELLOW}将依次运行 zero-shot 和 few-shot 测试...${NC}"
        echo ""
        
        # 运行zero-shot测试
        run_test "zeroshot"
        ZERO_EXIT=$?
        
        echo ""
        echo -e "${YELLOW}等待5秒后开始few-shot测试...${NC}"
        sleep 5
        echo ""
        
        # 运行few-shot测试
        run_test "fewshot"
        FEW_EXIT=$?
        
        # 如果任一测试失败，返回非零退出码
        if [ $ZERO_EXIT -ne 0 ] || [ $FEW_EXIT -ne 0 ]; then
            EXIT_CODE=1
        fi
        
        echo ""
        echo -e "${BLUE}========================================${NC}"
        echo -e "${BLUE}测试总结${NC}"
        echo -e "${BLUE}========================================${NC}"
        if [ $ZERO_EXIT -eq 0 ]; then
            echo -e "${GREEN}✅ Zero-shot测试: 成功${NC}"
        else
            echo -e "${RED}❌ Zero-shot测试: 失败${NC}"
        fi
        if [ $FEW_EXIT -eq 0 ]; then
            echo -e "${GREEN}✅ Few-shot测试: 成功${NC}"
        else
            echo -e "${RED}❌ Few-shot测试: 失败${NC}"
        fi
        ;;
esac

exit $EXIT_CODE

