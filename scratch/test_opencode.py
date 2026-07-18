import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("OPENCODE_API_KEY"),
    base_url="https://api.openai.com/v1" # We'll test different base_urls
)

def test_url(url, model):
    client.base_url = url
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Hello!"}],
            max_tokens=10
        )
        print(f"Success with {url} / {model}: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"Failed with {url} / {model}: {e}")
        return False

urls = [
    "https://api.opencode.so/v1",
    "https://api.opencode.ai/v1",
    "https://opencode.ai/zen/v1",
    "https://opencode.ai/zen/go/v1",
    "https://openrouter.ai/api/v1"
]

models = ["hy3", "hy3-free", "tencent/hy3:free", "tencent/hy3"]

for url in urls:
    for model in models:
        test_url(url, model)
