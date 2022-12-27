# Introduction

This is a markup tool through a telegram bot. The bot allows users to register, log in, and perform markup tasks. The bot also has an administrator service, which is a simple web app that allows the administrator to add pictures, classes, and launch tasks for ordinary users. The administrator can also view statistics on the marked data.

## Stack

- For the telegram bot, we have used python-telegram-bot
- For the backend, we have used Flask
- For the database, we have used Postgres
- For the Admin UI, we have used regular HTML with Jinja2 templating

## Features

- User registration and login
- Image markup tasks for users
- Administration service for adding pictures, classes, and launching tasks for ordinary users
- Statistics on marked data for administrators
- Downloading marked data for administrators

## Launch instructions
You will need to create a telegram bot if you don't have the secret key in order to get the telegram secret key. You can do this by following the instructions here: https://core.telegram.org/bots#6-botfather

Clone the repository to your local machine
Navigate to the root directory of the repository

To run all-in-one docker-compose, run the following command:
`docker-compose build`
`docker-compose up`

Which will run the PostgreSQL database at `postgres://postgres:postgres@localhost:5432/postgres`, the API at `http://localhost:5000`, and the telegram bot.
Access the application at http://localhost:5000


The bot can be accessed through the telegram app using the following link: t.me/DataMarkupBot
