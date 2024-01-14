# Testing ChatGPT-3.5-turbo API
# This is a very simple prompt query to test if the API works
#
# 2023, Ferris Kleier

import requests
import json
import secret


API_KEY = secret.get_apikey()
URL = secret.get_url()


role = 'You are an expert in categorizing posts from Stack Overflow. For a given post, decide if it contains the topic of configuration errors. If it does, respond with yes, if not, response with no'

data = {
    'messages': [{'role': 'system', 'content': role},
                 {'role': 'user', 'content': "I'm having some trouble with my Azure machine, it says a misconfiguration is causing trouble with the CPU load, can someone help me resolving this?"}],
}

url = URL
api_key = API_KEY


response = requests.post(url, headers={'Authorization': api_key}, json=data)
data = json.loads(response.text)
print(data['choices'][0]['message']['content'])
