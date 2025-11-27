# E-AGLE-Tonsi-IT-automation-Task1

## For the DB enviroment on Linux (I use Ubuntu)

1) Open a terminal
2) Install docker via the official guide at the following [link](https://docs.docker.com/engine/install/ubuntu/) (I use the following version: Docker version 29.0.4, it works also with the 29.1.0 version)
3) Install NocoDB using this [guide](https://nocodb.com/docs/self-hosting/installation/docker-compose)
4) Install python and pip (I use this version: Python 3.10.12)
5) Add your user to the docker group you can find the guide [here](https://docs.docker.com/engine/install/linux-postinstall/)
6) Move to the NocoDB directory inside the github repo
7) Run "docker compose up -d"
8) Open a browser on 'http://localhost:8080/'
9) Login with the credentials given in the .env file, if you don't have one, create your personal .env then login with yours credential. Pay attention on the name of the variables
10) Run the NocoDB_script.py via command "python3 NocoDB_script.py" or via VSCode (or another IDE, I use VS Code). If you create your personal .env you need to put all the API url necessary to the python script to work 
11) At this point the DB must be populated, if you don't see any changes reload the page

You can find an API documentation for NocoDB at the following [link](https://nocodb.com/apis/v2/data)

## For the telegram bot:

First setup the NocoDB enviroment if you want to use all the commands. If you don't setup the db you can encounter some issues.

1) Install the python-telegram-bot library via pip "pip install python-telegram-bot" (I use the 22.5 version). You can also setup a Python Virtual Enviroment (venv) here the [guide](https://www.hostinger.com/tutorials/how-to-create-a-python-virtual-environment?utm_campaign=Generic-Tutorials-DSA|NT:Se|Lang:EN|LO:IT&utm_medium=ppc&gad_source=1&gad_campaignid=21361943402&gclid=EAIaIQobChMIgIObu_aSkQMVgJ2DBx1Q3BGTEAAYASAAEgJJNPD_BwE). I install everything on my machine and not on the virtual enviroment because I have a lot of space.
2) Run the Telegram_script.py via command "python3 Telegram_script.py" or via VSCode (or another IDE, I use VS Code)
3) Go to the Telegram app and use this link 't.me/Daily_2_Bot'
4) Type /help to see the list of all commands available

