# Telegram Bot for Pizzeria

This telegram bot is for pizzeria menu. Also it represents admin access to pizzeria site

# How to Use

Step 1. Register new telegram bot for development purposes, get the new token. [@BotFather](https://telegram.me/botfather)
```
#!bash

$ # the token below is not actual, you need to register a new one
$ BOT_TOKEN="110831855:AAE_GbIeVAUwk11O12vq4UeMnl20iADUtM" python3 bot.py
```
Step 2. Launch (Use python virtual environment)

```bash
$ pip install -r requirements.txt
```
To init DB use 
```
(venv) $ flask db init
```
To upgrade DB description use
```
(venv) $ flask db upgrade
```
Export environment variable
```
$ export FLASK_APP=server.py
$ export SECRET_KEY='your secret key'
$ export BASIC_AUTH_PASSWORD='your admin password'
$ export BASIC_AUTH_USERNAME='your admin username'
```

Upload catalog to DB
```
$ python3 apply_data.py
```
To run aaplication on localhost use:
```bash
$ flask run
or
$ python3 server.py
```
Admin page will be able [here](http://127.0.0.1:5000/admin)

To run Bot use:
```bash
$ python3 bot.py
```
# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
