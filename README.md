# Perplexity API Interface

A Python client for interacting with the Perplexity AI chat completions API.

## Features

- Secure API key handling with encryption
- Support for both regular and streaming responses
- Configurable model parameters
- Built-in error handling and timeout management
- Environment variable configuration

## Environment Variables

Required environment variable in your .env file:
- PPLX_API_KEY (Generate your API key at Perplexity AI settings page)

## Installation

1. Clone the repository:
```
git clone https://github.com/mclaughco/perplexity-api.git
```

2. Install dependencies:
```
pip install -r requirements.txt
```

## Configuration Options

The API client supports various configuration parameters:
- Model selection
- Temperature control
- Token limits
- Presence and frequency penalties
- Search domain and recency filters
- Related questions and image return options

## Usage

Basic example:
```
from perplexity_api import PerplexityAPI

client = PerplexityAPI()
response = client.query(
    prompt="Your question here",
    system_prompt="Be precise and concise."
)
```

## Authors
- @seanm603

## License
MIT License
```