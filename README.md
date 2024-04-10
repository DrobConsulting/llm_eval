# Zero Shot MBPP Reproduction Using Code Llama

This project aims to reproduce the Zero Shot MBPP (Massive Bank of Problems in Programming) results as described in the "Code Llama: Open Foundation Models for Code" paper. We utilize the powerful capabilities of the Code Llama model to explore innovative approaches in code generation and comprehension.

![Code Llama Model Visualization](https://github.com/DrobConsulting/llm_eval/assets/35468552/2691a60c-4f23-46a3-9886-6a8b71ea1bac)

## Prerequisites

Before running the code, ensure you have a Lorax Predibase server operational. Follow the steps below to set up the server environment suitable for your needs.

### Setting Up Lorax Predibase Server

#### For Bit-Sand Quantization:

```bash
docker run --runtime=nvidia -e PORT="8080" -p 8080:8080 -v $volume:/data ghcr.io/predibase/lorax:latest --model-id codellama/CodeLlama-7b-Instruct-hf --max-input-length 512 --max-batch-prefill-tokens 1024 --quantize bitsandbytes-nf4
```

#### For No Quantization (13B Model):
```bash
docker run --runtime=nvidia -e PORT="8080" -p 8080:8080 -v $volume:/data ghcr.io/predibase/lorax:latest --model-id codellama/CodeLlama-13b-Instruct-hf --max-input-length 512 --max-batch-prefill-tokens 1024
```

#### Running the Tests
To validate the setup and ensure everything is working as expected, run the unit tests using the following command:

```bash
pytest
```

#### Usage
Running Pass1 Script
To execute the Pass1 script, use the following command. This will also log the output to a file for further analysis.

```bash
python3 async_main_pass1.py | tee 7B_np4_pass1.log
```
Running Pass10 Script
Similarly, to run the Pass10 script, use the following command:

```bash
python3 async_main_pass10.py | tee 7B_np4_pass10.log
```

#### Maintainer
This project is maintained by Michael Drob. For inquiries or contributions, please reach out through ![LinkedIn](https://www.linkedin.com/in/michael-drob/).


