import openai
import time

class ChatGpt3:
    def __init__(self, api):
        openai.api_key = api
        self.messages = [{"role": "system", "content": "You are a helpful assistant."}]  # Создаем список для хранения истории запросов

    def generate_response(self, user_message, max_tokens=10):
        """
        Генерирует ответ на заданный запрос.

        :param user_message: Текст запроса пользователя.
        :param max_tokens: Максимальное количество токенов в ответе (по умолчанию 10).
        :return: Сгенерированный ответ от GPT-3.
        """
        
        # Создаем сообщение пользователя и добавляем его в историю
        user_message_obj = {"role": "user", "content": user_message}
        self.messages.append(user_message_obj)
        
        
        
        # Отправляем запрос к GPT-3 с историей чата
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",  # Используйте актуальную версию модели GPT-3
            messages=self.messages
            
        )
        
        answer = response['choices'][0]['message']['content']
        # Добавляем ответ ассистента в историю
        self.messages.append({"role": "assistant", "content": answer})

        return answer
    
    # def generatedAnswerFromFile(self, user_message):
    #     user_message_obj = {"role": "user", "content": user_message}
    #     self.messages.append(user_message_obj)
    
    #     # Отправляем запрос к GPT-3 с историей чата
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo-16k",  # Используйте актуальную версию модели GPT-3
    #         messages=self.messages
    #     )
        
    #     answer = response['choices'][0]['message']['content']
    #     # Добавляем ответ ассистента в историю
    #     self.messages.append({"role": "assistant", "content": answer})

    #     return answer
    
    def loadFileInOpenai(self, filename):
        openai.File.create(
            file = open(filename, "rb"),
            purpose='fine-tune'
        )
        
        
        
        
            

    



# api = "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"
# test = ChatGpt3(api)

# test.loadFileInOpenai("test2.jsonl")


# prompt1 = 'Отвечай только на ангдийском'
# prompt2 = 'Напиши привет'

# m = test.generate_response(prompt1)
# print(m)
# c = test.generate_response(prompt2)
# print(c)
# m = test.generate_response(prompt1)
# print(m)
# c = test.generate_response(prompt2)
# print(c)