from email.quoprimime import quote
import json, requests, asyncio, random, discord
from aiohttp import BodyPartReader
import os
from discord.ui import Button, View
from googleapiclient.discovery import build

youtube_api_key = 'AIzaSyAgZ3rxMZWji3S51TCM7PYEEQAdvNnumQM'
daily_dose_playlist_id = 'PLlUZ3i-FUgHqk9-C-Fw_C6YsvTyx2c8nc'
pamela_reif_playlist_id = 'UUhVRfsT_ASBZk10o0An7Ucg'
youtube = build('youtube', 'v3', developerKey=youtube_api_key)


async def daily_dose(ctx):
    nextPageToken = None
    video_list = []
    while True:
        pl_request = youtube.playlistItems().list(
            part='snippet',
            playlistId = daily_dose_playlist_id,
            maxResults=50,
            pageToken=nextPageToken
        )

        pl_response = pl_request.execute()

        for item in pl_response['items']:
            video_list.append((item['snippet']['title'], 
                                item['snippet']['thumbnails'], 
                                item['snippet']['resourceId']['videoId']))

        nextPageToken = pl_response.get('nextPageToken')

        if not nextPageToken:
            video_num = random.randrange(len(video_list))
            embed=discord.Embed(title=video_list[video_num][0], url=str("https://youtube.com/watch?v="+video_list[video_num][2]), color=0x447ccf)
            embed.set_image(url=video_list[video_num][1]['standard']['url'])
            embed.set_author(name="Daily Dose Of Internet", url="https://www.youtube.com/c/DailyDoseOfInternet")
            await ctx.channel.send(embed=embed)
            break

async def daily_exercise(ctx):
    nextPageToken = None
    video_list = []
    while True:
        pl_request = youtube.playlistItems().list(
            part='snippet',
            playlistId = pamela_reif_playlist_id,
            maxResults=50,
            pageToken=nextPageToken
        )

        pl_response = pl_request.execute()

        for item in pl_response['items']:
            video_list.append((item['snippet']['title'], 
                                item['snippet']['thumbnails'], 
                                item['snippet']['resourceId']['videoId']))

        nextPageToken = pl_response.get('nextPageToken')

        if not nextPageToken:
            video_num = random.randrange(len(video_list))
            embed=discord.Embed(title="**Random Exercise: {}**".format(video_list[video_num][0]), url=str("https://youtube.com/watch?v="+video_list[video_num][2]), color=0xf52c80)
            embed.set_image(url=video_list[video_num][1]['standard']['url'])
            embed.set_author(name="Pamela Reif", url="https://www.youtube.com/channel/UChVRfsT_ASBZk10o0An7Ucg")
            await ctx.channel.send(embed=embed)
            break

async def get_data(link):
    response = requests.get(link)
    data = json.loads(response.text)
    return data

async def daily_bored(ctx):
    data = await get_data("https://www.boredapi.com/api/activity/")
    embed=discord.Embed(title="Random Activity", description=str(data["activity"]), color=0x1d339f)
    await ctx.author.send(embed=embed)

async def daily_quote(ctx):
    data = await get_data("https://zenquotes.io/api/random")
    embed=discord.Embed(title="Random Quote",description="**{}**\n\t-{}".format(data[0]["q"], data[0]["a"]))
    await ctx.channel.send(embed=embed)

async def daily_recipe(ctx):
    data = await get_data("https://www.themealdb.com/api/json/v1/1/random.php")
    embed=discord.Embed(title="Random Recipe: **{}**".format(data["meals"][0]["strMeal"]),url=data["meals"][0]["strYoutube"])
    embed.set_image(url=data["meals"][0]["strMealThumb"])
    await ctx.channel.send(embed=embed)

async def daily_cat(ctx):
    data = await get_data("https://catfact.ninja/fact")
    embed=discord.Embed(title="Random Cat Fact", description=str(data["fact"]), color=0x1d339f)
    await ctx.author.send(embed=embed)

async def daily_dog(ctx):
    data = await get_data("https://dog-api.kinduff.com/api/facts")
    embed=discord.Embed(title="Random Dog Fact", description=str(data["facts"][0]), color=0x1d339f)
    await ctx.author.send(embed=embed)



async def daily_pref(ctx, preferences):
    preferences[ctx.author.id]["b"] = False 
    preferences[ctx.author.id]["q"] = False
    preferences[ctx.author.id]["r"] = False
    preferences[ctx.author.id]["c"] = False
    preferences[ctx.author.id]["dd"] = False
    preferences[ctx.author.id]["e"] = False

    embed=discord.Embed(title="Please Select Your Daily Preferences", description="Using >my daily will send you all your preferences :D", color=0x1d339f)
    
    bored =     Button(label = "Activity", style=discord.ButtonStyle.green, emoji="⚒")
    quote =     Button(label = "Quote", style=discord.ButtonStyle.green, emoji="🎭")
    recipe =    Button(label = "Recipe", style=discord.ButtonStyle.green, emoji="🍜")
    cat =       Button(label = "Cat", style=discord.ButtonStyle.green, emoji="😺")
    dog =       Button(label = "Dog", style=discord.ButtonStyle.green, emoji="🐶")
    dd =        Button(label = "Daily Dose", style=discord.ButtonStyle.green, emoji="📮")
    exercise =  Button(label = "Exercse", style=discord.ButtonStyle.green, emoji="💪")

    async def d_b(interaction):
        await interaction.response.defer()
        bored.disabled = True
        preferences[ctx.author.id]["b"] = True
        await interaction.message.edit(view=reg_daily)

    async def d_q(interaction):
        await interaction.response.defer()
        quote.disabled = True
        preferences[ctx.author.id]["q"] = True
        await interaction.message.edit(view=reg_daily)
    
    async def d_r(interaction):
        await interaction.response.defer()
        recipe.disabled = True
        preferences[ctx.author.id]["r"] = True
        await interaction.message.edit(view=reg_daily)
    
    async def d_c(interaction):
        await interaction.response.defer()
        cat.disabled = True
        preferences[ctx.author.id]["c"] = True
        await interaction.message.edit(view=reg_daily)
        
    async def d_d(interaction):
        await interaction.response.defer()
        dog.disabled = True
        preferences[ctx.author.id]["d"] = True
        await interaction.message.edit(view=reg_daily)
        
    async def d_dd(interaction):
        await interaction.response.defer()
        dd.disabled = True
        preferences[ctx.author.id]["dd"] = True
        await interaction.message.edit(view=reg_daily)
        
    async def d_e(interaction):
        await interaction.response.defer()
        exercise.disabled = True
        preferences[ctx.author.id]["e"] = True
        await interaction.message.edit(view=reg_daily)

    bored.callback = d_b
    quote.callback = d_q
    recipe.callback = d_r
    cat.callback = d_c
    dog.callback = d_d
    dd.callback = d_dd
    exercise.callback = d_e

    reg_daily = View()
    reg_daily.add_item(bored)
    reg_daily.add_item(quote)
    reg_daily.add_item(recipe)
    reg_daily.add_item(cat)
    reg_daily.add_item(dog)
    reg_daily.add_item(dd)
    reg_daily.add_item(exercise)
    
    await ctx.author.send(embed=embed, view=reg_daily)







