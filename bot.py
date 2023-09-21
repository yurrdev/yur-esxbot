
from operator import itemgetter
import discord 
from discord.ext import commands 
from discord.ext import *
import json 
from pathlib import Path 
import platform 
import logging
import mysql.connector
from typing import Tuple, Any, Optional, Union
from discord.ext.commands.cooldowns import BucketType
import random
import string
import datetime
from discord import Embed

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="es_extended"
)

cursor = conn.cursor()
cwd = Path(__file__).parents[0]
cwd = str(cwd)
print(f"{cwd}\n-----")


secret_file = json.load(open(cwd+'/bot_config/secrets.json'))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True, owner_id=1024976155603906620)
bot.config_token = secret_file['token']
logging.basicConfig(level=logging.INFO)

bot.version = '1.0'



@bot.event
async def on_ready():
    print(f"-----\nLogged in as: {bot.user.name}")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="👀The Server"))
    

@bot.event
async def on_command_error(ctx, error):
    
    ignored = (commands.CommandNotFound, commands.UserInputError)
    if isinstance(error, ignored):
        return

    
    if isinstance(error, commands.CommandOnCooldown):
        m, s = divmod(error.retry_after, 60)
        h, m = divmod(m, 60)
        if int(h) == 0 and int(m) == 0:
            await ctx.send(f' You must wait {int(s)} seconds to use this command!')
        elif int(h) == 0 and int(m) != 0:
            await ctx.send(f' You must wait {int(m)} minutes and {int(s)} seconds to use this command!')
        else:
            await ctx.send(f' You must wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!')
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("Hey! You lack permission to use this command.")
    raise error









@bot.command()
async def money(ctx):
    
    discord_id = str(ctx.author.id)

    
    discord_id = 'discord:' + discord_id

    try:
       
        cursor.execute("SELECT accounts FROM users WHERE discord = %s", (discord_id,))
        result = cursor.fetchone()

        if result is not None:
            accounts_data = json.loads(result[0])  
            
 
            cash = accounts_data['money']
            bank = accounts_data['bank']
            black_money = accounts_data['black_money']  
            
         
            embed = discord.Embed(title=f"{ctx.author.name}'s Money Balance", color=0x00ff00)
            embed.set_image(url="https://www.nedbank.co.sz/content/dam/africa/Swaziland/Site_Assets/images/hero-images/Coming-soon-Banner-05.jpg")
            embed.add_field(name="Cash", value=f"${cash}", inline=False)
            embed.add_field(name="Bank", value=f"${bank}", inline=False)
            embed.add_field(name="Black Money", value=f"${black_money}", inline=False)  

            await ctx.send(embed=embed)
        else:
            await ctx.send("No data found for your Discord ID in the database.")
    except Exception as e:
        print(f"An error occurred: {e}")
        await ctx.send("An error occurred while fetching your money data.")







@bot.command()
async def givecash(ctx, amount: int, recipient: discord.Member):
    
    sender_id = 'discord:' + str(ctx.author.id)
    
    cursor.execute("SELECT accounts FROM users WHERE discord = %s", (sender_id,))
    sender_result = cursor.fetchone()
    if sender_result is not None:
        sender_accounts_data = json.loads(sender_result[0])
        sender_cash = sender_accounts_data.get("money", 0)
        
        recipient_id = 'discord:' + str(recipient.id)
        cursor.execute("SELECT accounts FROM users WHERE discord = %s", (recipient_id,))
        recipient_result = cursor.fetchone()
        if recipient_result is not None:
            recipient_accounts_data = json.loads(recipient_result[0])
            recipient_cash = recipient_accounts_data.get("money", 0)
            
            if sender_cash < amount:
                await ctx.send("You don't have enough cash to make this transfer.")
                return

            sender_accounts_data['money'] = sender_cash - amount
            recipient_accounts_data['money'] = recipient_cash + amount

            sql = "UPDATE users SET accounts = %s WHERE discord = %s"
            val = (json.dumps(sender_accounts_data), sender_id)
            cursor.execute(sql, val)
            conn.commit()

            sql = "UPDATE users SET accounts = %s WHERE discord = %s"
            val = (json.dumps(recipient_accounts_data), recipient_id)
            cursor.execute(sql, val)
            conn.commit()
            
            embed = discord.Embed(title="Money Transfer", color=0x00ff00)
            embed.add_field(name="Sender", value=ctx.author.name, inline=False)
            embed.add_field(name="Recipient", value=recipient.name, inline=False)
            embed.add_field(name="Amount", value=f"${amount}", inline=False)
            embed.set_image(url="https://img.freepik.com/premium-vector/money-transfer-mobile-phone-application-financial-transaction-money-onlineonline-payment-financial-savings-business-finance-capital-flow-website-banner-isometric-vector-illustration_473922-14.jpg?w=2000")

            await ctx.send(embed=embed)
        else:
            await ctx.send("No data found for the recipient's Discord ID in the database.")
    else:
        await ctx.send("No data found for your Discord ID in the database.")





@bot.command()
async def inventory(ctx):
    discord_id = 'discord:' + str(ctx.author.id)
    cursor.execute("SELECT inventory FROM users WHERE discord = %s", (discord_id,))  
    result = cursor.fetchone()
    if result is not None:
        inventory_data = json.loads(result[0])  

        embed = discord.Embed(title="Inventory", color=0x00ff00)
        
        
        for item in inventory_data:
            name = item["name"]
            amount = item["count"]  
            embed.add_field(name=name, value=f"Amount: {amount}", inline=False)

        await ctx.send(embed=embed)
    else:
        await ctx.send("No data found for your Discord ID in the database.")






@bot.command()
async def carshop(message):
    cursor.execute("SELECT name, price FROM vehicles")
    result = cursor.fetchall()
    
    response = "Los Santos Car Dealer:\n"
    for car in result:
        new_line = f"{car[0]} - ${car[1]}\n"
        
        
        if len(response) + len(new_line) > 1800:
           
            await message.channel.send(response)
            response = ""
        
        response += new_line
    
    
    if response:
        await message.channel.send(response)








@bot.command()
async def buycar(ctx, model: str, custom_plate: str):

    discord_id = 'discord:' + str(ctx.author.id)

    cursor.execute("SELECT identifier, accounts FROM users WHERE discord = %s", (discord_id,))
    result = cursor.fetchone()
    
    if result is not None:
        identifier = result[0]
        accounts_data = json.loads(result[1])
        
        available_cash = accounts_data.get('money', 0)
        
        cursor.execute("SELECT price FROM vehicles WHERE model = %s", (model,))
        result = cursor.fetchone()

        if result is not None:
            price = result[0]

            if available_cash < price:
                await ctx.send("You don't have enough cash to buy this car.")
                return

            accounts_data['money'] -= price
            cursor.execute("UPDATE users SET accounts = %s WHERE identifier = %s", (json.dumps(accounts_data), identifier))
            conn.commit()

            default_vehicle_data = {
                "modTurbo": False,
                "modDoorR": -1,
                "modSmokeEnabled": False,
               
                "model": model,
                "plate": custom_plate,
                "fuelLevel": 100,
                
            }

            sql = "INSERT INTO owned_vehicles (owner, model, vehicle, plate, garage, paidprice, stored) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (identifier, model, json.dumps(default_vehicle_data), custom_plate, 'A', price, 1)
            cursor.execute(sql, val)
            conn.commit()


            embed = Embed(title="Purchase Confirmation", description="You have successfully bought a new car!", color=0x00ff00)
            embed.add_field(name="Model:", value=model, inline=True)
            embed.add_field(name="Price:", value=f"${price}", inline=True)
            embed.add_field(name="Plate:", value=custom_plate, inline=True)
            embed.add_field(name="New Owner:", value=ctx.author.mention, inline=True)
            embed.set_image(url="https://cdn.dribbble.com/users/515394/screenshots/5084521/car_loop_4x3.gif")

            await ctx.send(embed=embed)

        else:
            await ctx.send("The specified car model could not be found in the database.")
            
    else:
        await ctx.send("No data found for your Discord ID in the database.")








@bot.command()
async def findbot(ctx):
    bot_list = []
    
    for member in ctx.guild.members:
        if member.bot:
            bot_list.append(member.name)
    
    if bot_list:
        embed = Embed(title="List of Bots", description="\n".join(bot_list), color=0x00ff00)
        await ctx.send(embed=embed)
    else:
        await ctx.send("No bots found in this server.")








bot.run(bot.config_token) 