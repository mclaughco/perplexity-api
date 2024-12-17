MIT License

Copyright (c) 2024 Sean

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

# Perplexity API Interface

This is a [Go](https://go.dev/doc/) script for interacting with the [Perplexity AI](https://docs.perplexity.ai/home) chat completions API via the CLI.



## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`PPLX_API_KEY`

[Generate an API key](https://www.perplexity.ai/settings/api)
## Deployment

Clone the repository

```bash
  git clone https://github.com/mclaughco/perplexity-api.git
```
Add your `.env` file
```bash
touch .env
echo "PPLX_API_KEY={your-key}" >> .env
```
Run it
```bash
go run perplexity.go
```
## Authors

- [@seanm603](https://www.github.com/seanm603)


requests==2.26.0
python-dotenv==1.0.0

from setuptools import setup, find_packages

setup(
    name="perplexity-api",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.26.0",
        "perplexipy>=1.1.3"
    ],
)
import os
import json
import requests
from typing import Dict, Optional



class PerplexityAPI:
    def __init__(self, api_key: Optional[str])
def main():
    """Main entry point for the application."""
    try:
       print("Hello, World!") 
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
