import g4f.cookies
from g4f.client import Client
import base64


# Dictionary mapping model names to provider names
model_provider_mapping = {
    'gpt-3.5-turbo': 'DDG',
    'gpt-4o': None,
    'mixtral_8x7b': 'HuggingFace',
    'blackbox': 'Blackbox',
    'meta': 'MetaAI',
    'llama3_70b_instruct': 'MetaAI',
    # Add more models and providers as needed
}

# Dictionary mapping display model names to internal model names
display_model_mapping = {
    'gpt 3.5 turbo': 'gpt-3.5-turbo',
    'gpt 4o': 'gpt-4o',
    'llama 3': 'llama3_70b_instruct',
    'Mixtral 70b': 'mixtral_8x7b',
    'BlackBox': 'blackbox',
    'Meta AI': 'meta',
}


def get_provider(model: str) -> str:
    """Get provider name based on the model."""
    return model_provider_mapping.get(model, '')


def get_model(display_model: str) -> str:
    """Get internal model name based on the display model name."""
    return display_model_mapping.get(display_model, '')


def get_bot_response(prompt, internal_model, provider_name):
        client = Client()
        response = client.chat.completions.create(
            model=internal_model,
            messages=[{"role": "user", "content": prompt}],
            provider=provider_name,
            cookies=g4f.cookies.get_cookies('bing')
        )
        return response.choices[0].message.content


