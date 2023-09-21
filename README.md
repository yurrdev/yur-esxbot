# Yur ESX Bot!

This is a Discord bot designed to interface with the ES Extended (esx) framework for FiveM. It provides various commands allowing users to interact with the game server, fetching player information, server status, etc., directly from Discord.

## Features
- Fetches player money balances (cash, bank, and black money).
- Easily extendable to add more commands and features.
- Uses Cogs for organizing command and event listeners.

## Prerequisites
- Python 3.6 or higher.
- Discord.py library.
- MySQL Connector Python.

## Setup
1. Clone this repository to your local machine.
   ```sh
   git clone <repository_url>
   cd <repository_directory>

## SETUP TOKEN
{
  "token": "YOUR_DISCORD_BOT_TOKEN"
}


Configure the database connection in the bot's source code.

## SETUP SQL CONNECTION
db_config = {
  "host": "localhost",
  "user": "root",
  "password": "YOUR_DB_PASSWORD",
  "database": "es_extended"
}

## Usage
!money: Displays the user's in-game money balances.
More commands can be added easily as per your requirements.


## Contributing
Fork the Project.
Create your Feature Branch (git checkout -b feature/AmazingFeature).
Commit your Changes (git commit -m 'Add some AmazingFeature').
Push to the Branch (git push origin feature/AmazingFeature).
Open a Pull Request.
