import os
import subprocess
import telebot
from telebot import types
from app.aiGen.chatGPT import ChatGpt3
from app.aiGen.imageGen import ImageGen

from dotenv import load_dotenv

class TelegramBot():
    def __init__(self, token, user_id) -> None:
        self.bot = telebot.TeleBot(token=token, parse_mode=None)
        self.user_id = user_id
        self.selected_command = {}
        self.bot.send_message(self.user_id, "Сервер запущен и его можно вырубить)")
        self.prompt = None
        load_dotenv()
        self.chat_gpt_token = os.getenv("CHAT_GPT_TOKEN")
        
        
        @self.bot.message_handler(commands=['start', 'menu'])
        def show_menu(message):
            if message.from_user.id == self.user_id:
                markup = types.InlineKeyboardMarkup(row_width=2)
                item1 = types.InlineKeyboardButton("Выкл ПК", callback_data='shutdown')
                item2 = types.InlineKeyboardButton("Подготовить рабочее место", callback_data='command1')
                item3 = types.InlineKeyboardButton("Chat GPT 3", callback_data="chatgpt3")
                item4 = types.InlineKeyboardButton("OpenAI Gen Image", callback_data="openaiGenImage")
                
                markup.add(item1, item2, item3, item4)
                self.bot.send_message(message.chat.id, "Выберите команду:", reply_markup=markup)
            else:
                self.bot.send_message(message.chat.id, "Извините, вы не имеете доступ к этой команде.")

        
        # Обработчик обратных вызовов
        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_callback(call):
            
            chat_id = call.message.chat.id
            message_id = call.message.message_id

            if call.data == 'shutdown':
                self.selected_command[chat_id] = 'shutdown'
                self.bot.send_message(chat_id, "Введите 'д' для подтверждения.")

            elif call.data == 'command1':
                self.selected_command[chat_id] = 'command1'
                self.bot.send_message(chat_id, "Введите 'д' для подтверждения.")
            
            elif call.data == 'chatgpt3':
                self.bot.send_message(chat_id, "Добро пожаловть в чат с нейросетью. Напишите свой запрос")
                self.selected_command[chat_id] = 'chatgpt3'
                
            elif call.data == 'openaiGenImage' :
                self.bot.send_message(chat_id, "Добро пожаловть для генерации картинок. Напишите свой запрос")
                self.selected_command[chat_id] = 'openaiGenImage'
        
            elif "gptImageRes" in call.data:
                resolution = call.data.split(',')[1]  # Извлекаем разрешение из callback_data
                self.bot.send_message(chat_id, f"Выбрано разрешение: {resolution}")
                response = ImageGen.generate_response(self.chat_gpt_token, prompt=self.prompt, size=resolution)  # Передаем разрешение в функцию
                self.bot.send_photo(chat_id, response)
                
                
                

        # Обработчик подтверждения команды
        @self.bot.message_handler(func=lambda message: self.selected_command.get(message.chat.id) is not None)
        def confirm_command(message):
            chat_id = message.chat.id
            if self.selected_command[chat_id] == 'chatgpt3':
                user_message = message.text
                chat_gpt = ChatGpt3()
                response = chat_gpt.generate_response(self.chat_gpt_token, user_message)  # Используйте метод из класса ChatGpt3
                self.bot.send_message(chat_id, response)
            
            
            elif self.selected_command[chat_id] == 'openaiGenImage':
                self.prompt = message.text
                # Словарь с вариантами разрешений
                resolutions = ["256x256", "512x512", "1024x1024"]
                markup = types.InlineKeyboardMarkup(row_width=1)
                for resolution in resolutions:
                    button = types.InlineKeyboardButton(resolution, callback_data=f'gptImageRes,{resolution}')
                    markup.add(button)

                # Отправляем сообщение с инлайн-кнопками
                self.bot.send_message(chat_id, "Выберите разрешение изображения:", reply_markup=markup)
                

            elif message.text.lower() == 'д':
                command = self.selected_command.pop(chat_id)
                if command == 'shutdown':
                    self.bot.send_message(chat_id, "Ваш пк скоро будет выключен")
                    subprocess.run(["shutdown", "/s", "/t", "1"])
                elif command == 'command1':
                    self.bot.send_message(chat_id, "Скоро подготовиться ваше рабочее место")
                    subprocess.run(["C:\\Program Files\\Mozilla Firefox\\firefox.exe"])
                    subprocess.run(["C:\\Users\\tonips\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"])
            else:
                self.selected_command.pop(chat_id)
                self.bot.send_message(chat_id, "Отменено. Выбранная команда не будет выполнена.")

        # Обработчик колбэк данных
        @self.bot.callback_query_handler(func=lambda call: True)
        def handle_resolution_callback(call):
            self.bot.send_message(self.user_id, "Разрешение выбрано)")
            chat_id = call.message.chat.id
            message_id = call.message.message_id
            print(f"User selected resolution: {call.data}")
            
            
            user_message = self.user_message
            response = ImageGen.generate_response(self.chat_gpt_token, user_message='cat' )
            self.bot.send_photo(chat_id, response)
            

    def start_polling(self):
        self.bot.infinity_polling()
