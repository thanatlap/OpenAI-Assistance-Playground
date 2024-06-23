
# OpenAI Customer Service Assistant
This project provides a Python script that interfaces with the OpenAI API to handle common customer service inquiries. The script takes a user's question as input, uses the OpenAI GPT model to generate a response, checks the response for appropriateness, and then presents the formatted response to the user.

## Features
- Handles common customer service inquiries.
- Utilizes OpenAI's `gpt-3.5-turbo` model.
- Checks responses for appropriateness using OpenAI's Moderation API.
- Provides detailed error handling and retries up to three times if a response is flagged as inappropriate.

## Installation
1. Clone repository
```shell
git clone https://github.com/thanatlap/OpenAI-Assistance-Playground.git
```
2. Install the required Python packages
```shell
pip install -r requirements.txt
```

## Usage
To run the script, use the following command:
```shell
python main.py \
--api_key <openai_api_key> \
--api_endpoint https://api.openai.com/v1/chat/completions \
--moderation_endpoint https://api.openai.com/v1/moderations
```