import json

MODELS_TOP1 = [
  {
    "name": "custom-model",
    "displayName": "Code Llama 13b Instruct",
    "description": "This is a custom model configured to work with my local server.",
    "preprompt": "Use Python: ",
    "chatPromptTemplate": "[INST] {{content}} [/INST]",
    "parameters": {
      "temperature": 0.1,
      "top_p": 0.95,
      "repetition_penalty": 1.2,
      "top_k": 50,
      "truncate": 1024,
      "do_sample": False,
      "max_new_tokens": 1024,  # Adjusted to match your server setup
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
    "displayName": "Code Llama 13b Instruct",
    "description": "This is a custom model configured to work with my local server.",
    "preprompt": "Use Python: ",
    "chatPromptTemplate": "[INST] {{content}} [/INST]",
    "parameters": {
      "temperature": 0.8,
      "top_p": 0.95,
      "repetition_penalty": 1.2,
      "top_k": 50,
      "truncate": 1024,
      "do_sample": True,
      "max_new_tokens": 1024,  # Adjusted to match your server setup
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