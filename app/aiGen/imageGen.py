import openai
import os

class ImageGen:
    @staticmethod
    def generate_response(api_key, prompt, n=1, size="1024x1024", max_tokens=10):
        openai.api_key = api_key
        
        response = openai.Image.create(
        prompt=prompt,
        n=n, # количество картинок
        size=size
        )
        return response['data'][0]['url']
    