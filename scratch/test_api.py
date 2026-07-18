import os
from google import genai

client = genai.Client(
    api_key="AQ.Ab8RN6K1qMEKOHqNQUtmJ38F1BoK-QPBgenOEugDe18BBtekWQ"
)

tools = [
    {
        'type': 'google_search',
    },
]

generation_config = {
    'temperature': 1,
    'max_output_tokens': 65536,
    'top_p': 0.95,
}

interaction = client.interactions.create(
    model='models/gemini-3.1-flash-lite',
    input='',
    tools=tools,
    generation_config=generation_config,
)

print(interaction.steps[-1])


