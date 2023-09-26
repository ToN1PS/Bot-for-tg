# app/commands.py

def show_help(update, context):
    help_message = (
        "Доступные команды:\n"
        "/start - Начать использование бота\n"
        "/shutdown - Выключить компьютер\n"
        "/help - Показать это сообщение с командами"
    )
    update.message.reply_text(help_message)

