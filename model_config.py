import json

MODELS_TOP1 = [
  {
    "name": "custom-model",
    "displayName": "Code Llama Instruct",
    "description": "This is a custom model configured to work with my local server.",
    "preprompt": "",
    "chatPromptTemplate": '[INST] You are an expert Python programmer, and here is your task: {task}\nYour code should pass these tests:\n\n{tests}\nYour code should start with a [PYTHON] tag and end with a [/PYTHON] tag.\n [/INST]',
    "parameters": {
      "temperature": 0.001,
      "top_p": 0.95,
      "repetition_penalty": 1.2,
      "top_k": 100,
      "truncate": 512,
      "do_sample": False,
      "max_new_tokens": 512,  # Adjusted to match your server setup
      "stop_sequences": ["</s>"]
    },
    "promptExamples": [
      # Add your custom prompt examples here
    ],
    "endpoints": [{
      "type": "tgi",
      "url": "http://localhost:8080",
    }]
  }
]

MODELS_TOPK = [
  {
    "name": "custom-model",
    "displayName": "Code Llama Instruct",
    "description": "This is a custom model configured to work with my local server.",
    "preprompt": "",
    "chatPromptTemplate": '[INST] You are an expert Python programmer, and here is your task: {task}\nYour code should pass these tests:\n\n{tests}\nYour code should start with a [PYTHON] tag and end with a [/PYTHON] tag.\n [/INST]',
    "parameters": {
      "temperature": 0.8,
      "top_p": 0.95,
      "repetition_penalty": 1.2,
      "top_k": 100,
      "truncate": 512,
      "do_sample": True,
      "max_new_tokens": 512,  # Adjusted to match your server setup
      "stop_sequences": ["</s>"]
    },
    "promptExamples": [
      # Add your custom prompt examples here
    ],
    "endpoints": [{
      "type": "tgi",
      "url": "http://localhost:8080",
    }]
  }
]
