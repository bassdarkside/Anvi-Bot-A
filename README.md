# Anvi-Bot-A

Anvi-Bot-A - this is a Telegram-bot of the "Fluffy wildebeest" team for purchasing cosmetics from the site `https://anvibodycare.com`

---
### Get the repository
Clone the repository -> navigate to the cloned folder -> install `requirments.txt`:
```sh
git clone https://github.com/bassdarkside/Anvi-Bot-A.git
cd Anvi-Bot-A
pip install -r requirments.txt
```
---
## Before you start 
### Setting up `.env` file

The `.env.txt` example file is located in the `bot_start` directory.  
>1. Rename `.env.txt` file to `.env` and open.
>2. Put Telegram API Token
>3. Replace `'XXXX'` (I will send the chat **ID** upon request).  
---
>**Listen Chat** _<https://t.me/+loCzklVYXz5hOTJi>_.

![how to](img/how-to-env.png?raw=true "Title")

### To use features for admins, you need to add your Telegram ID to `.env `.  
    ADMIN = XXXXXXXXX

#### after that you can use command:
    /admin

## Start the bot   

File `run.py` starting parser and bot:
```sh
python run.py
```

### The catalog is updated once a day at `06:00` Kyiv time


## Change log
-    Add variations items for "Hair" category
-    Add "About" and "Contacts" buttons  
- ...