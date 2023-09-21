# Yur ESX Bot!

This is a Discord bot designed to interface with the ES Extended (esx) framework for FiveM. It provides various commands allowing users to interact with the game server, fetching player information, server status, etc., directly from Discord.

## Features
- Database Integration: The bot connects to a MySQL database (es_extended) using the mysql.connector library to store and retrieve user data, including accounts and inventory information.

Command Handling: The bot uses the discord.ext.commands extension to handle and execute commands issued by users in a Discord server.

Money Balance: Users can check their in-game money balance with the !money command. The bot retrieves this information from the database and displays it in an embedded message.

Money Transfer: Users can transfer in-game money to other players using the !givecash command. The bot verifies the sender's balance and updates the recipient's balance accordingly in the database.

Inventory Display: The !inventory command allows users to view their in-game inventory. The bot retrieves the inventory data from the database and presents it in an embedded message.

Car Shop Listing: Users can view a list of available cars in a car dealership using the !carshop command. The bot fetches this information from the database and sends a message with car names and prices.

Car Purchase: With the !buycar command, users can buy cars from the car dealership. The bot verifies the user's balance, deducts the purchase price, and adds the car to the user's owned vehicles in the database.

Bot List: The !findbot command allows users to list all bots present in the Discord server.

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
