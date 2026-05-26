# ProOPF: Benchmarking and Improving LLMs for Professional-Grade Power Systems Optimization Modeling

This project provides a comprehensive benchmarking framework for evaluating and improving Large Language Models (LLMs) in power systems optimization modeling tasks.

## 📁 Project Structure

```
.
├── LLM_test/                    # Test scripts directory
│   ├── test_level1.py          # Level 1 test script (supports zero-shot and few-shot)
│   ├── test_level2.py          # Level 2 test script (supports zero-shot and few-shot)
│   ├── test_level3.py          # Level 3 test script (supports zero-shot and few-shot)
│   └── test_level4.py          # Level 4 test script (supports zero-shot and few-shot)
├── Scripts/                     # Shell scripts directory
│   ├── run_level1_test.sh      # Level 1 automated test script
│   ├── run_level2_test.sh      # Level 2 automated test script
│   ├── run_level3_test.sh      # Level 3 automated test script
│   └── run_level4_test.sh      # Level 4 automated test script
├── ProOPF_B/                    # Benchmark dataset directory
│   ├── level1_with_labels.jsonl
│   ├── level2_with_labels.jsonl
│   ├── level3_with_labels.jsonl
│   └── level4_with_labels.jsonl
├── ProOPF_D/                    # Few-shot example data directory
│   ├── level1_data_example.jsonl
│   ├── level2_data_example.jsonl
│   ├── level3_data_example.jsonl
│   └── level4_data_example.jsonl
├── base_test_output/            # Test results output directory
└── .vscode/                     # VS Code debug configuration
    └── launch.json              # Debug launch configuration
```

## 🎯 Benchmark Level Description

The benchmark consists of four levels based on the degree of expert knowledge required to translate a natural language request into an executable OPF formulation. We consider two orthogonal dimensions: (1) whether parameter modifications Δπ are explicitly specified in the problem description P or should be inferred from scenario-dependent operational descriptions, and (2) whether a structural modification s ∈ S is required beyond the base OPF model. The Cartesian product of these two binary dimensions yields four difficulty levels that systematically cover the modeling action space Ωπ × (S ∪ {∅}), spanning a progressive spectrum from basic modification to expert-level model adaptation.

### Level 1: Explicit Parameter Modification, No Structural Modification
- **Task Type**: Generate complete MATPOWER scripts where parameter modifications Δπ are explicitly specified in the problem description P, with no structural modifications to the base OPF model
- **Difficulty**: Basic
- **Features**: Parameter values are directly provided in the natural language request. Requires understanding of basic MATPOWER usage, ability to correctly load case files, apply explicit parameter modifications, and run standard OPF

### Level 2: Inferred Parameter Modification, No Structural Modification
- **Task Type**: Generate MATLAB functions where parameter modifications Δπ must be inferred from scenario-dependent operational descriptions, with no structural modifications to the base OPF model
- **Difficulty**: Intermediate
- **Features**: Parameters need to be extracted and interpreted from contextual operational scenarios rather than being explicitly stated. Requires generating functions that conform to naming conventions, including parameter validation and assertion checks, and the ability to translate operational requirements into specific parameter values

### Level 3: Explicit Parameter Modification, Structural Modification Required
- **Task Type**: Generate complete scripts where parameter modifications Δπ are explicitly specified, but structural modifications s ∈ S are required beyond the base OPF model (e.g., DC OPF, custom objective functions, additional constraints, etc.)
- **Difficulty**: Advanced
- **Features**: While parameters are explicitly given, the model structure must be adapted. Requires handling complex optimization model settings, including custom objective functions, constraint modifications, and model transformations while applying the specified parameter changes

### Level 4: Inferred Parameter Modification, Structural Modification Required
- **Task Type**: Generate complete scripts where both parameter modifications Δπ must be inferred from scenario-dependent operational descriptions and structural modifications s ∈ S are required beyond the base OPF model
- **Difficulty**: Expert-level
- **Features**: Requires the highest level of expertise: simultaneously inferring parameters from operational context and adapting the model structure. This level demands deep understanding of power systems operations, optimization modeling, and the ability to translate complex operational scenarios into both appropriate parameter values and corresponding structural model modifications

## 🔧 Environment Requirements

### Required Dependencies
- Python 3.7+
- MATLAB R2018b+ (requires MATLAB Python engine installation)
- The following Python packages:
  ```bash
  pip install requests orjson
  ```

### MATLAB Python Engine Installation
1. **Linux/Mac**:
   ```bash
   cd <MATLAB installation path>/extern/engines/python
   python setup.py install
   ```

2. **Windows**:
   ```cmd
   cd <MATLAB installation path>\extern\engines\python
   python setup.py install
   ```

Example paths:
- Mac: `/Applications/MATLAB_R20XXx.app/extern/engines/python`
- Linux: `/usr/local/MATLAB/R20XXx/extern/engines/python`
- Windows: `C:\Program Files\MATLAB\R20XXx\extern\engines\python`

## ⚙️ Configuration

### Method 1: Environment Variables (Recommended)

Before use, please set the following environment variables:

```bash
# Set API key
export LLM_API_KEY="your-api-key-here"

# Set API base URL
export LLM_BASE_URL="https://api.example.com/v1"

# Set default model name (optional)
export LLM_MODEL_NAME="your-model-name"
```

### Method 2: Command Line Arguments

All API configurations can be passed via command line arguments. See usage instructions below for details.

## 🚀 Usage

### Method 1: Using Shell Scripts (Recommended, Simplest)

Shell scripts provide the most convenient testing method, supporting both zero-shot and few-shot modes.

#### Basic Usage

```bash
# Navigate to Scripts directory
cd Scripts

# Add execute permissions to scripts (Linux/Mac)
chmod +x run_level1_test.sh run_level2_test.sh run_level3_test.sh run_level4_test.sh

# Run Level 1 test (API information needs to be configured first)
./run_level1_test.sh --model YOUR_MODEL_NAME --api-key YOUR_API_KEY --base-url YOUR_API_BASE_URL

# Run Level 2 test
./run_level2_test.sh --model YOUR_MODEL_NAME --api-key YOUR_API_KEY --base-url YOUR_API_BASE_URL

# Run Level 3 test
./run_level3_test.sh --model YOUR_MODEL_NAME --api-key YOUR_API_KEY --base-url YOUR_API_BASE_URL

# Run Level 4 test
./run_level4_test.sh --model YOUR_MODEL_NAME --api-key YOUR_API_KEY --base-url YOUR_API_BASE_URL
```

#### Using Environment Variables (More Concise)

```bash
# First set environment variables
export LLM_API_KEY="your-api-key"
export LLM_BASE_URL="https://api.example.com/v1"
export LLM_MODEL_NAME="your-model-name"

# Then run directly (scripts will automatically read environment variables)
./run_level1_test.sh
```

#### Test Mode Selection

```bash
# Run zero-shot test only
./run_level1_test.sh --zero-shot --model MODEL_NAME --api-key API_KEY --base-url BASE_URL

# Run few-shot test only
./run_level1_test.sh --few-shot --model MODEL_NAME --api-key API_KEY --base-url BASE_URL

# Run both zero-shot and few-shot tests (default)
./run_level1_test.sh --both --model MODEL_NAME --api-key API_KEY --base-url BASE_URL
```

#### Other Common Options

```bash
# Specify test range (test samples 1 to 10)
./run_level1_test.sh --start 1 --end 10 --model MODEL_NAME --api-key API_KEY --base-url BASE_URL

# Enable debug mode
./run_level1_test.sh --debug --model MODEL_NAME --api-key API_KEY --base-url BASE_URL

# Use thinking model (longer timeout and more tokens)
./run_level1_test.sh --thinking --model MODEL_NAME --api-key API_KEY --base-url BASE_URL
```

#### View Help Information

```bash
./run_level1_test.sh --help
```

### Method 2: Using Python Scripts (More Flexible)

#### Zero-shot Mode

```bash
# Level 1 Zero-shot test
python LLM_test/test_level1.py \
    --output base_test_output/level1_test_{model}_zeroshot_output.jsonl \
    --model YOUR_MODEL_NAME \
    --input-file ProOPF_B/level1_with_labels.jsonl \
    --api-key YOUR_API_KEY \
    --base-url YOUR_API_BASE_URL

# Level 2 Zero-shot test
python LLM_test/test_level2.py \
    --output base_test_output/level2_test_{model}_zeroshot_output.jsonl \
    --model YOUR_MODEL_NAME \
    --input-file ProOPF_B/level2_with_labels.jsonl \
    --api-key YOUR_API_KEY \
    --base-url YOUR_API_BASE_URL

# Level 3 Zero-shot test
python LLM_test/test_level3.py \
    --output base_test_output/level3_test_{model}_zeroshot_output.jsonl \
    --model YOUR_MODEL_NAME \
    --input-file ProOPF_B/level3_with_labels.jsonl \
    --api-key YOUR_API_KEY \
    --base-url YOUR_API_BASE_URL

# Level 4 Zero-shot test
python LLM_test/test_level4.py \
    --output base_test_output/level4_test_{model}_zeroshot_output.jsonl \
    --model YOUR_MODEL_NAME \
    --input-file ProOPF_B/level4_with_labels.jsonl \
    --api-key YOUR_API_KEY \
    --base-url YOUR_API_BASE_URL
```

#### Few-shot Mode

```bash
# Level 1 Few-shot test
python LLM_test/test_level1.py \
    --output base_test_output/level1_test_{model}_fewshot_output.jsonl \
    --model YOUR_MODEL_NAME \
    --input-file ProOPF_B/level1_with_labels.jsonl \
    --few-shot \
    --example-file ProOPF_D/level1_data_example.jsonl \
    --api-key YOUR_API_KEY \
    --base-url YOUR_API_BASE_URL

# Level 2 Few-shot test
python LLM_test/test_level2.py \
    --output base_test_output/level2_test_{model}_fewshot_output.jsonl \
    --model YOUR_MODEL_NAME \
    --input-file ProOPF_B/level2_with_labels.jsonl \
    --few-shot \
    --example-file ProOPF_D/level2_data_example.jsonl \
    --api-key YOUR_API_KEY \
    --base-url YOUR_API_BASE_URL

# Level 3 Few-shot test
python LLM_test/test_level3.py \
    --output base_test_output/level3_test_{model}_fewshot_output.jsonl \
    --model YOUR_MODEL_NAME \
    --input-file ProOPF_B/level3_with_labels.jsonl \
    --few-shot \
    --example-file ProOPF_D/level3_data_example.jsonl \
    --api-key YOUR_API_KEY \
    --base-url YOUR_API_BASE_URL

# Level 4 Few-shot test
python LLM_test/test_level4.py \
    --output base_test_output/level4_test_{model}_fewshot_output.jsonl \
    --model YOUR_MODEL_NAME \
    --input-file ProOPF_B/level4_with_labels.jsonl \
    --few-shot \
    --example-file ProOPF_D/level4_data_example.jsonl \
    --api-key YOUR_API_KEY \
    --base-url YOUR_API_BASE_URL
```

#### Other Common Parameters

```bash
# Specify test range
python LLM_test/test_level1.py \
    --output output.jsonl \
    --model MODEL_NAME \
    --start 1 \
    --end 10 \
    --api-key API_KEY \
    --base-url BASE_URL

# Enable debug mode
python LLM_test/test_level1.py \
    --output output.jsonl \
    --model MODEL_NAME \
    --debug \
    --api-key API_KEY \
    --base-url BASE_URL

# Use thinking model
python LLM_test/test_level1.py \
    --output output.jsonl \
    --model MODEL_NAME \
    --thinking \
    --api-key API_KEY \
    --base-url BASE_URL
```
## 📊 Output Format

Test results are saved in JSONL format, with one JSON object per line containing the following fields:

```json
{
    "sample_id": 1,
    "status": "correct" | "incorrect",
    "natural_language": "Problem description",
    "ground_truth": {
        "objective_value": 1234.56,
        "converged": true  // Level 2 and Level 3 include this field
    },
    "model_output": {
        "objective_value": 1234.57,
        "success": true  // Level 2 and Level 3 include this field
    },
    "llm_raw_output": "Raw output text from LLM",
    "complete_matlab_code": "Extracted complete MATLAB code",
    "error": null,  // If there is an error, error information will be included here
    "token_limit_exceeded": false
}
```

## 🔍 Error Handling Strategy

- **API call failure**: Automatically retry up to 3 times, terminate test after 3 failures (failed data not saved)
- **Code extraction failure**: Continue testing and save error data
- **MATLAB execution failure**: Continue testing and save error data
- **Result mismatch**: Continue testing and save error data

## 📈 Statistics

After testing completes, the script will output statistics including:
- Total number of samples
- Number and percentage of correct answers
- Number and percentage of incorrect answers
- Error details (if any)

## 💡 Tips

1. **First-time use**: It is recommended to test a single sample first using `--start 1 --end 1` to ensure correct configuration
2. **API quota**: Pay attention to API call quota limits to avoid exceeding limits and causing test interruption
3. **MATLAB path**: Ensure MATLAB is correctly installed and added to system PATH
4. **Output directory**: Test results are saved in real-time, so completed data will not be lost even if interrupted
5. **Model selection**: Different models may perform very differently, it is recommended to test multiple models for comparison

## 🤝 Contributing

Welcome to submit Issues and Pull Requests!


