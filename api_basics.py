from openai import OpenAI
import time
import re
from config import TEMPERATURE, MAX_TOKENS

# UTSA API configuration
UTSA_API_KEY = "utsa-08GdYYyq2lzmWc02fhfMSKzv3ACPwYgq6U02BozaaupZym1wGQzJBNC59dV4wFTi"
UTSA_BASE_URL = "http://149.165.171.140:8888/v1"
UTSA_MODEL = "Qwen/Qwen3-8B"

# Client oluştur
client = OpenAI(
    base_url=UTSA_BASE_URL,
    api_key=UTSA_API_KEY
)


def query_llm(prompt, temperature=TEMPERATURE, max_tokens=MAX_TOKENS):

    start_time = time.time()

    response = client.chat.completions.create(
        model=UTSA_MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant. Do not include internal reasoning."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )

    latency = time.time() - start_time

    full_response = response.choices[0].message.content

    # remove <think> blocks
    cleaned = re.sub(r"<think>.*?</think>", "", full_response, flags=re.DOTALL)

    # remove reasoning phrases
    cleaned = re.sub(r"Okay.*?\n", "", cleaned)
    cleaned = re.sub(r"Let me.*?\n", "", cleaned)

    return {
        "text": cleaned.strip(),
        "latency": latency

    }