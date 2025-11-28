# E-AGLE Tonsi – IT Automation Task 1  
Setup Guide for **NocoDB + Telegram Bot** on Linux (Ubuntu)

## Database Environment Setup (NocoDB on Linux)

> **Requirements:** Ubuntu

---

## **1) Install Docker**
Open a terminal and install Docker following the official guide:  
https://docs.docker.com/engine/install/ubuntu/

**Tested versions:**  
- Docker **29.0.4**  
- Docker **29.1.0**

---

## **2) Install NocoDB**
Follow the official installation guide:  
https://nocodb.com/docs/self-hosting/installation/docker-compose

You can find an additional API documentation for NocoDB at the following [link](https://nocodb.com/apis/v2/data)

---

## **3) Install Python and Required Libraries**
Install **Python 3.10+**, **pip**, and **python-dotenv**:

```bash
sudo apt install python3 python3-pip
pip install python-dotenv
```

Optional but recommended: create a Python virtual environment (venv).  
Guide: https://www.hostinger.com/tutorials/how-to-create-a-python-virtual-environment

---

## **4) Add Your User to the Docker Group**
Follow the official post-installation steps:  
https://docs.docker.com/engine/install/linux-postinstall/

This allows Docker to run without `sudo`.

---

## **5) Download the GitHub Repository**
Clone using a terminal:

```bash
git clone <REPOSITORY_URL>
```

or download via the GitHub interface.

---

## **6) Clean NocoDB Directories**
Inside the repository, go to the `NocoDB/` directory and remove all `.gitkeep` files from empty folders:

Directories that must NOT contain `.gitkeep`:

```
nc_data/_data
db_data/pg_commit_ts
db_data/pg_dynshmem
db_data/pg_notify
db_data/pg_replslot
db_data/pg_serial
db_data/pg_snapshots
db_data/pg_stat
db_data/pg_stat_tmp
db_data/pg_tblspc
db_data/pg_twophase
```

---

## **7) Create Required Logical Directories**
Inside `NocoDB/db_data/pg_logical/`, create two directories:

```
snapshots
mappings
```

---

## **8) Start NocoDB via Docker**
Move into the `NocoDB/` folder using the terminal and run:

```bash
docker compose up -d
```

The containers will start in detached mode.

---

## **9) Access the NocoDB Web Interface**
Open your browser and go to:

```
http://localhost:8080/
```

---

## **10) Login and Configure Environment Variables**
Login using the credentials defined in your `.env` file.

If you do NOT have a `.env`:

1. Create your personal `.env` in the same directory as the Python scripts.  
2. Ensure all required variables (API URLs, authentication keys, etc.) are included.  
3. Make sure variable names match exactly what the Python scripts expect.

Missing or incorrect variables will cause the population script to fail.

---

## **11) Populate the Database**
Run the script:

```bash
python3 NocoDB_script.py
```

or execute it in VS Code (or another IDE).

If the data does not appear immediately, refresh the browser page.

**Important:**  
Do **not** delete the **Lessons** table.  
The Telegram bot relies on it for the `/lessons` command.

---

# Telegram Bot Setup

> To access all bot commands, make sure your NocoDB environment is correctly configured and it is running.

---

## **1) Install python-telegram-bot**
Recommended version: **22.5**

```bash
pip install python-telegram-bot==22.5
```

---

## **2) Run the Telegram Bot Script**

```bash
python3 Telegram_script.py
```

---

## **3) Access the Bot on Telegram**
Open the link:

```
t.me/Daily_2_Bot
```

---

## **4) View Available Commands**
In the Telegram chat, type:

```
/help
```
