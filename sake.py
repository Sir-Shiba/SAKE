import discord, urllib.parse, asyncio, random, json, os, requests
import sake_help as help
import sake_daily as daily
# from discord.ext.commands import bot
# from discord.ext import commands
from discord.ui import Button, View, Select
from collections import defaultdict
from copy import deepcopy
from google.cloud import storage

#   discord intitalization
token = open('token1.txt', 'r').read()
intents = discord.Intents()
intents.messages = True 
intents.message_content = True
client = discord.Client(intents=intents)

#   cloud initialization
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "sake-discord-82675aa87cf1.json"
storage_client = storage.Client()

#   uploading from cloud
def upload_to_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        print(e)
        return False

#   downloading from cloud
def download_from_bucket(blob_name, file_path, bucket_name):
    try:
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        with open(file_path, 'wb') as f:
            storage_client.download_blob_to_file(blob, f)
    except Exception as e:
        print(e)
        return False

#   intial cloud download
download_from_bucket('ME LMAO', 'data.json', 'sake_discord_bot')
with open('data.json') as json_file:
    info = json.load(json_file)

registration = defaultdict(list , info["regis"])
preferences = defaultdict(lambda: defaultdict(lambda: False), info["pref"])

to_cloud = {"regis": dict(registration), "pref": dict(preferences)}

#   On bot startup
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('A Bot made for You and Me <3\nUse >help for help'))
    print(f'{client.user} has connected to Discord!')

#   On seeing a message
@client.event
async def on_message(ctx):
    print(f"{ctx.channel.id}: {ctx.author}: {ctx.author.name} {ctx.author.id}: {ctx.content}")
    
    msg = str(ctx.content)
    print('Message Sent:', msg)

    if msg.startswith('>'):
        command = msg[1:]
        print("Command Issued:", command)

        #   Section on Help

        if command.lower() == "register":
            await help.register(ctx, registration, client)
            await asyncio.sleep(30)
            to_cloud = {"regis": dict(registration), "pref": dict(preferences)}
            with open('data.json', 'w') as fp:
                json.dump(to_cloud, fp,  indent=4)
    
        elif command.lower() == "connect":
            await help.serious(ctx, registration)
        
        if command.lower() == "remove":
            await help.reg_remove(registration, ctx)

        if command.lower() == "report":
            await help.report(ctx, client)
        
        #   Section on Daily

        if command.lower() == "activity":
            await daily.daily_bored(ctx)

        if command.lower() == "quote":
            await daily.daily_quote(ctx)

        if command.lower() == "recipe":
            await daily.daily_recipe(ctx)
        
        if command.lower() == "cat":
            await daily.daily_cat(ctx)

        if command.lower() == "dog":
            await daily.daily_dog()

        if command.lower() == "dailydose":
            await daily.daily_dose(ctx)

        if command.lower() == "exercise":
            await daily.daily_exercise(ctx)

        # registers to send curated things
        if command.lower() == "regdaily":
            await daily.daily_pref(ctx, preferences)
            await asyncio.sleep(30)
            to_cloud = {"regis": dict(registration), "pref": dict(preferences)}
            with open('data.json', 'w') as fp:
                json.dump(to_cloud, fp,  indent=4)

        if command.lower() == "mydaily":
            if ctx.author.id not in list(preferences.keys()):
                embed = discord.Embed(title="Please use >regdaily to register first ❤")
                await ctx.author.send(embed = embed)
            else:
                if preferences[ctx.author.id]["b"]: 
                    await daily.daily_bored(ctx)
                if preferences[ctx.author.id]["q"]: 
                    await daily.daily_quote(ctx)
                if preferences[ctx.author.id]["r"]: 
                    await daily.daily_recipe(ctx)
                if preferences[ctx.author.id]["c"]: 
                    await daily.daily_cat(ctx)
                if preferences[ctx.author.id]["d"]: 
                    await daily.daily_dog(ctx)
                if preferences[ctx.author.id]["dd"]: 
                    await daily.daily_dose(ctx)
                if preferences[ctx.author.id]["e"]: 
                    await daily.daily_exercise(ctx)
                
        if command.lower() == "dailyall":
            await daily.daily_bored(ctx)
            await daily.daily_quote(ctx)
            await daily.daily_recipe(ctx)
            await daily.daily_cat(ctx)
            await daily.daily_dog(ctx)
            await daily.daily_dose(ctx)
            await daily.daily_exercise(ctx)

        if command.lower() == "weather":
            await ctx.channel.send("Please enter your location with no spaces in between.")
            msg = await client.wait_for("message", check=lambda message: message.author == ctx.author)
            try:
                response = requests.get(f"https://weatherdbi.herokuapp.com/data/weather/{str(msg.content)}")
                data = json.loads(response.text)
                embed=discord.Embed(title=data["region"],description="@ "+data["currentConditions"]["dayhour"]+":\n"+
                                    str(data["currentConditions"]["temp"]["f"])+"°F\n"+data["currentConditions"]["comment"])
                embed.set_thumbnail(url=data["currentConditions"]["iconURL"])
                await ctx.channel.send(embed=embed)
            except: await ctx.channel.send("Try again. Please check your spelling and spacing.")
    
        if command.lower() == "image":
            await ctx.channel.send("Who or what would you like to search up?")
            msg = await client.wait_for("message", check=lambda message: message.author == ctx.author)
            response = requests.get(f"https://imsea.herokuapp.com/api/1?q={str(msg.content)}")
            data = json.loads(response.text)
            embed=discord.Embed()
            embed.set_image(url=random.choice(data["results"]))
            await ctx.channel.send(embed=embed)

        if command.lower() == "covid":
            response = requests.get("https://covid2019-api.herokuapp.com/v2/total")
            data = json.loads(response.text)
            embed=discord.Embed(title="🦠Worldwide Covid Live Tracker🦠")
            embed.add_field(name="Confirmed: ", value=str(data["data"]["confirmed"]))
            embed.add_field(name=chr(173),value=chr(173))
            embed.add_field(name=chr(173),value=chr(173))
            embed.add_field(name="Deaths: ", value=str(data["data"]["deaths"]))
            embed.add_field(name=chr(173),value=chr(173))
            embed.add_field(name=chr(173),value=chr(173))
            embed.add_field(name="Last Updated: ", value=str(data["dt"]))
            await ctx.channel.send(embed=embed)
    
        if command.lower() == "translate":
            await ctx.channel.send("Enter any text and I will translate it to English.")
            msg = await client.wait_for("message", check=lambda message: message.author == ctx.author)
            response = requests.get(f"https://api.popcat.xyz/translate?to=en&text={msg.content}")
            data = json.loads(response.text)
            await ctx.channel.send(data["translated"])

        #help pages
        if command.lower() == "help":
            await help.help_commands(ctx)

        if command.lower() == "update":
            to_cloud = {"regis": dict(registration), "pref": dict(preferences)}
            with open('data.json', 'w') as fp:
                json.dump(to_cloud, fp,  indent=4)

            to_cloud = {"regis": dict(registration), "pref": dict(preferences)}
            upload_to_bucket('ME LMAO', "data.json", "sake_discord_bot")

client.run(token)