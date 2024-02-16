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


import asyncio
from model_config import MODELS_TOPK
from datasets import load_dataset
from utils import eval_llm_top_k, eval_llm_output, generate_and_evaluate_problems_async
from lorax import AsyncClient

k=10
MODELS = MODELS_TOPK
client = AsyncClient(MODELS[0]["endpoints"][0]["url"])

def load_data():
    return load_dataset("mbpp")  # Synchronously load the dataset outside async function

async def main():
    dataset = load_data()  # Load the dataset once, synchronously
    await generate_and_evaluate_problems_async(dataset, MODELS, client, k)

if __name__ == "__main__":
    asyncio.run(main())