from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

import os
from openai import OpenAI

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

client = OpenAI(
base_url="https://router.huggingface.co/v1",
api_key = HF_TOKEN,
)

completion = client.chat.completions.create(
model="HuggingFaceH4/zephyr-7b-beta:featherless-ai", # Only works if you have access
messages=[
    {
    "role": "user",
    "content": "What is the capital of France?"
    }
],
)

print(completion.choices[0].message)