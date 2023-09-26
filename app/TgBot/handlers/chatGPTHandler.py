from app.aiGen.chatGPT import ChatGpt3

class ChatGptHandler:
    def __init__(self, chat_gpt_token, telegram_bot):
        self.chat_gpt_token = chat_gpt_token
        

    def generate_response(self, user_message):
        chat_gpt = ChatGpt3()
        response = chat_gpt.generate_response(self.chat_gpt_token, user_message)
        # Отправляем ответ в TelegramBot
        
