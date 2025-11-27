import os
import requests
import asyncio
import json
from telegram import *
from telegram.ext import *
from datetime import datetime
from dotenv import *

# Load the enviroment variable
load_dotenv()
header = json.loads(os.getenv("headers"))

# Variable for the adduser command
(NAME, SURNAME, STATE, PERSONAL_EMAIL, 
 UNIVERSITY_EMAIL, PHONE_NUMBER, TELEGRAM_USER, 
 DEPARTMENT, AREA, ENTRY_DATE, EXIT_DATE, SEX, 
 DATE_BIRTH) = range(13)

#------------------------------------------------------------------------------------------------------------------------------------------

# Definition of the adduser command
async def addUser_cmd (update: Update, context:ContextTypes.DEFAULT_TYPE):
    """This command allow you to add a user to the database"""
    await update.message.reply_text("Write the name of the new user:")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["NAME"] = update.message.text
    await update.message.reply_text("Write the surname:")
    return SURNAME

async def get_surname(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["SURNAME"] = update.message.text
    await update.message.reply_text("Write the state of the member:")
    return STATE

async def get_state(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["STATE"] = update.message.text
    await update.message.reply_text("Write the personal email:")
    return PERSONAL_EMAIL

async def get_personal_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["PERSONAL_EMAIL"] = update.message.text
    await update.message.reply_text("Write the university email:")
    return UNIVERSITY_EMAIL

async def get_university_email(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["UNIVERSITY_EMAIL"] = update.message.text
    await update.message.reply_text("Write the phone number:")
    return PHONE_NUMBER

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["PHONE_NUMBER"] = update.message.text
    await update.message.reply_text("Write the telegram username (without the @):")
    return TELEGRAM_USER

async def get_telegram_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["TELEGRAM_USER"] = "@" + update.message.text
    await update.message.reply_text("Write the department:")
    return DEPARTMENT

async def get_department(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["DEPARTMENT"] = update.message.text
    await update.message.reply_text("Write the area:")
    return AREA

async def get_area(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["AREA"] = update.message.text
    await update.message.reply_text("Write the entry date (AAAA-MM-GG):")
    return ENTRY_DATE

async def get_entry_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["ENTRY_DATE"] = update.message.text
    await update.message.reply_text("Write the exit date (AAAA-MM-GG) o 'N/A':")
    return EXIT_DATE

async def get_exit_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["EXIT_DATE"] = update.message.text
    if context.user_data["EXIT_DATE"] == "N/A":
        context.user_data["EXIT_DATE"] = None
    await update.message.reply_text("Write the sex (Male/Female/Other):")
    return SEX

async def get_sex(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["SEX"] = update.message.text
    await update.message.reply_text("Write the date birth (AAAA-MM-GG):")
    return DATE_BIRTH

async def get_date_birth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["DATE_BIRTH"] = update.message.text
    # Build the json for the db
    user = {
        "State": context.user_data.get("STATE", ""),
        "Name": context.user_data.get("NAME", ""),
        "Surname": context.user_data.get("SURNAME", ""),
        "Personal Email": context.user_data.get("PERSONAL_EMAIL", ""),
        "University Email": context.user_data.get("UNIVERSITY_EMAIL", ""),
        "Phone Number": context.user_data.get("PHONE_NUMBER", ""),
        "Telegram Username": context.user_data.get("TELEGRAM_USER", ""),
        "Department": context.user_data.get("DEPARTMENT", ""),
        "Entry Date": context.user_data.get("ENTRY_DATE", ""),
        "Exit Date": context.user_data.get("EXIT_DATE", ""),
        "Sex": context.user_data.get("SEX", ""),
        "Date of Birth": context.user_data.get("DATE_BIRTH", ""),
        "Area": context.user_data.get("AREA", "")
    }
    
    api_url_users = f"{os.getenv('url_users')}"
    api_url_area = f"{os.getenv('url_areas')}"
    api_url_departments = f"{os.getenv('url_departments')}"

    # Insert the values inside the table
    upload_response = requests.post(api_url_users, headers = header, json = user)

    # Return value
    if upload_response.status_code != 200:
        await update.message.reply_text ("Upload failed:" + upload_response.text)
    else:
        await update.message.reply_text ("Upload completed")

    get_response = requests.get(api_url_area, headers=header)
    if get_response.status_code != 200:
        print ("Get request failed:", get_response.text)
    else:
        print ("Get request completed")
    areas = get_response.json()["list"]

    get_response = requests.get(api_url_departments, headers=header)

    if get_response.status_code != 200:
        print ("Get request failed:", get_response.text)
    else:
        print ("Get request completed")

    departments = get_response.json()["list"]

    # Get the user ID
    get_response = requests.get(api_url_users, headers=header)

    if get_response.status_code != 200:
        print ("Get request failed:", get_response.text)
    else:
        print ("Get request completed")

    users = get_response.json()["list"]

    # Make a control to extract the IDs for the link
    user_ID = ""
    department_ID = ""
    area_ID = ""
    last_user = users[0]

    for u in users:
        if last_user["Id"] < u["Id"]:
            last_user = u
            user_ID = u["Id"]

    for d in departments:
        if (last_user["Department"] == d["Name"]):
            department_ID = d["Id"]
    
    user_area = last_user["Area"].split()
    tag = user_area[0]
    for a in areas:
        if (tag == a["Tag"]):
            area_ID = a["Id"]
    
    user_ID = str (user_ID)
    area_ID = str (area_ID)
    department_ID = (department_ID)
    # Linking the area
    url_link_users = f"{os.getenv('BASE_URL')}{os.getenv('LINK_URL_AREA')}{user_ID}"
    payload = {"Id": area_ID} 
    upload_response = requests.post(url_link_users, headers=header, json=payload)
    if upload_response.status_code != 201:
        await update.message.reply_text ("Area link for user: " + user_ID + " failed")
        exit
    else:
        await update.message.reply_text ("Area link for user: " + user_ID + " completed")

    # Linking the department
    url_link_users = f"{os.getenv('BASE_URL')}{os.getenv('LINK_URL_DEPARTMENT')}{user_ID}"  
    payload = {"Id": department_ID} 
    upload_response = requests.post(url_link_users, headers=header, json=payload)
    if upload_response.status_code != 201:
        await update.message.reply_text ("Department link for user: " + user_ID + " failed")
        exit
    else:
        await update.message.reply_text ("Department link for user: " + user_ID + " completed")



async def annulla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END


#--------------------------------------------------------------------------------------------------------------------------------

# A small function that return the Schedule value
def schedule(s):
    return s['Schedule']

# Definition od the lessons command
async def lesson_cmd(update: Update, context:ContextTypes.DEFAULT_TYPE):
    """This command return all the today lessons"""
    # Take the today date
    today = datetime.now()
    name = today.strftime("%A")
    
    # Request to get the lessons from the DB
    api_url_lessons = os.getenv("url_lessons")
    get_response = requests.get(api_url_lessons, headers=header)
    if get_response.status_code != 200:
        print ("Get request failed:", get_response.text)
    else:
        print ("Get request completed")

    lessons = get_response.json()["list"]

    # Extract the today lessons based on the day (Monday, Tuesday,...)
    today_lessons = []
    for l in lessons:
        if l["Day"] == name:
            today_lessons.append(l)
    text = ""
    # Sort the lessons by their schedule
    today_lessons.sort(key=schedule)

    # Construct the message to print out
    for item in today_lessons:
        text += (
            f"*- Subject:* {item['Subject']}\n"
            f"    Room: {item['Rooom']}\n"
            f"    Schedule: {item['Schedule']}"
            "\n \n"
    )
    
    # Return the message with all the today lessons
    await update.message.reply_text(text, parse_mode="Markdown")

#-------------------------------------------------------------------------------------------------------------------

# Definition of help command, with all the commands available
async def help_cmd(update: Update, context:ContextTypes.DEFAULT_TYPE):
    """This command return a list of all usable commands and a description"""
    commands = []
    # Read the "static" command
    for handler in context.application.handlers[0]:
        if isinstance(handler, CommandHandler):
            cmd = list(handler.commands)[0]
            doc = handler.callback.__doc__ or ''
            commands.append(f"/{cmd} - {doc}")
    # Read the conversation command
    if isinstance(handler, ConversationHandler):
        for entry in handler.entry_points:
            if isinstance(entry, CommandHandler):
                cmd = list(entry.commands)[0]
                doc = entry.callback.__doc__ or ''
                commands.append(f"/{cmd} - {doc}")

    text = "Available commands: \n" + "\n \n".join(commands)
    await update.message.reply_text(text)

#-------------------------------------------------------------------------------------------------------------------------------

# Definition of start command
async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """This command start the chat with the bot"""
    await update.message.reply_text("Hello! 👋 \n Type the /help command for the list of all usable commands!")

#---------------------------------------------------------------------------------------------------------------------------------------------
