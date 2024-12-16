
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

