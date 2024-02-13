import asyncio
from model_config import MODELS_TOP1
from datasets import load_dataset
from utils import eval_llm_top_k, eval_llm_output, generate_and_evaluate_problems_async
from lorax import AsyncClient

MODELS = MODELS_TOP1
client = AsyncClient(MODELS[0]["endpoints"][0]["url"])

def load_data():
    return load_dataset("mbpp")  # Synchronously load the dataset outside async function

async def main():
    dataset = load_data()  # Load the dataset once, synchronously
    await generate_and_evaluate_problems_async(dataset, MODELS, client)

if __name__ == "__main__":
    asyncio.run(main())