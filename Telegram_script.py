from src.Telegram_Bot_Function import *
from dotenv import *

# Load the enviroment variable
load_dotenv()

def main():
    app = ApplicationBuilder().token(os.getenv("API_BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("help",help_cmd))
    app.add_handler(CommandHandler("lessons",lesson_cmd))
    conv = ConversationHandler(
        entry_points=[CommandHandler("adduser", addUser_cmd)],
        states={
            NAME:            [MessageHandler(filters.TEXT, get_name)],
            SURNAME:         [MessageHandler(filters.TEXT, get_surname)],
            STATE:           [MessageHandler(filters.TEXT, get_state)],
            PERSONAL_EMAIL:  [MessageHandler(filters.TEXT, get_personal_email)],
            UNIVERSITY_EMAIL:[MessageHandler(filters.TEXT, get_university_email)],
            PHONE_NUMBER:    [MessageHandler(filters.TEXT, get_phone)],
            TELEGRAM_USER:   [MessageHandler(filters.TEXT, get_telegram_user)],
            DEPARTMENT:      [MessageHandler(filters.TEXT, get_department)],
            AREA:            [MessageHandler(filters.TEXT, get_area)],
            ENTRY_DATE:      [MessageHandler(filters.TEXT, get_entry_date)],
            EXIT_DATE:       [MessageHandler(filters.TEXT, get_exit_date)],
            SEX:             [MessageHandler(filters.TEXT, get_sex)],
            DATE_BIRTH:      [MessageHandler(filters.TEXT, get_date_birth)],
        },
        fallbacks=[CommandHandler("annulla", annulla)]
    )

    app.add_handler(conv)
    app.run_polling()

if __name__ == "__main__":
    main()