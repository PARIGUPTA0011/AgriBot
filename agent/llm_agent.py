# from huggingface_hub import InferenceClient
# import os
# from dotenv import load_dotenv

# # Load environment variables from .env file
# load_dotenv()
# HF_API_TOKEN = os.getenv("HF_TOKEN")

# # Create client with token
# client = InferenceClient(token=HF_API_TOKEN)

# # Use a public model available for Hosted Inference API
# MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"

# def generate_answer(context_list, user_question, max_new_tokens=300):
#     """
#     Generate a farmer-friendly answer in Hindi/English using the LLM.
#     """
#     context = "\n".join(context_list)
#     prompt = f"""Context:
# {context}

# Question: {user_question}
# Answer simply in Hindi/English for a farmer:
# """

#     response = client.text_generation(
#         model=MODEL_NAME,
#         prompt=prompt,
#         max_new_tokens=max_new_tokens,
#         temperature=0.7,
#         top_p=0.9
#     )
#     return response

from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
HF_API_TOKEN = os.getenv("HF_TOKEN")

# Create client with token
client = InferenceClient(token=HF_API_TOKEN)

# Use a public model available for Hosted Inference API
MODEL_NAME = "HuggingFaceH4/zephyr-7b-beta"

def generate_answer(context_list, user_question, max_new_tokens=300):
    """
    Generate a farmer-friendly answer in Hindi/English using the LLM.
    """
    context = "\n".join(context_list)

    # Instead of building a raw string prompt, send chat-style messages
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful agricultural assistant. "
                "Always explain solutions simply in Hindi mixed with easy English, "
                "so that a farmer can understand clearly."
            ),
        },
        {
            "role": "user",
            "content": f"""Here is some context from web pages:
{context}

My question: {user_question}

Answer clearly and practically for a farmer:""",
        },
    ]

    response = client.chat_completion(
        model=MODEL_NAME,
        messages=messages,
        max_tokens=max_new_tokens,
        temperature=0.7,
        top_p=0.9,
    )

    return response.choices[0].message["content"]
