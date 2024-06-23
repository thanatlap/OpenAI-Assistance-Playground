from typing import Dict, Optional
import os
import requests
import argparse


SYSTEM_PROMPT = (
    'You are a helpful assistant to handle '
    'common customer service inquiries. '
    'The response should be user-friendly '
    'and aligns with typical customer '
    'service etiquette'
    )


class OpenAIChat:
    def __init__(
        self, 
        api_key: str, 
        api_endpoint: str, 
        moderation_endpoint: str,
        system_prompt: str = SYSTEM_PROMPT,
        openai_model: str = 'gpt-3.5-turbo',
        max_attempt: int = 3
        ):
        self.api_key = api_key
        self.api_endpoint = api_endpoint
        self.moderation_endpoint =moderation_endpoint
        self.max_attempt = max_attempt
        self.system_prompt = system_prompt
        self.openai_model = openai_model

    
    @staticmethod
    def call_api(api_endpoint: str, headers: Dict[str, str], data: Dict[str, str])->Optional[Dict]:
        response = requests.post(api_endpoint, headers=headers, json=data)

        try: 
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            return None
        
        except requests.exceptions.RequestException as req_err:
            return None
        

    def openai_completion_api(self, user_query: str)->str:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

        data = {
            'model': self.openai_model,
            'messages': [
                {'role': 'system', 'content': self.system_prompt},
                {'role': 'user', 'content': user_query}
            ]
        }
        response = self.call_api(self.api_endpoint, headers, data)
        if response:
            return response['choices'][0]['message']['content']
        else:
            return 'Sorry, I am unable to process your request at the moment.'
        

    def is_appropriate(self, response: str)->bool:
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        data = {'input': response}
        response = self.call_api(self.moderation_endpoint, headers, data)
        if response:
            flagged = response['results'][0]['flagged']
            return not flagged
        else:
            return False
        

    def chat(self, user_query: str)->str:
        response = self.openai_completion_api(user_query)

        attempt = 1 
        while not self.is_appropriate(response):
            response = self.openai_completion_api(user_query)
            attempt += 1
            if attempt > self.max_attempt:
                return 'Sorry, I am unable to provide a suitable response at the moment.'
        return response
    

def user_input()->str:
    return input('SUPPORT: What can I assist you with today?\nUSER: ')


def format_output(response: str)->str:
    return f'SUPPORT: {response}'


if __name__=='__main__':
    parser = argparse.ArgumentParser(description='OpenAI Client')
    parser.add_argument('--api_key', type=str, required=True, help='OpenAI API Key')
    parser.add_argument('--api_endpoint', type=str, default='https://api.openai.com/v1/chat/completions', help='OpenAI API Endpoint')
    parser.add_argument('--moderation_endpoint', type=str, default='https://api.openai.com/v1/moderations', help='OpenAI Moderation Endpoint')
    args = parser.parse_args()

    openaichat = OpenAIChat(
        args.api_key, args.api_endpoint, args.moderation_endpoint
    )
    user_query = user_input()
    response = openaichat.chat(user_query)
    response = format_output(response)
    print(response)

    
