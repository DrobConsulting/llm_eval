"""
Author: Michael Drob
Contact: https://www.linkedin.com/in/michael-drob/
License: Apache 2.0

This program is free software: you can redistribute it and/or modify
it under the terms of the Apache License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
Apache License for more details.

You should have received a copy of the Apache License
along with this program. If not, see <http://www.apache.org/licenses/LICENSE-2.0>.
"""

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
