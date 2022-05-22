import discord, urllib.parse, asyncio, random, json
from discord.ui import Select, Button, View
from collections import defaultdict
from copy import deepcopy

from requests import options

async def send_names(ctx, registration, bool):
    embed=discord.Embed(title="Here are your Contacts", description="", color=0x1d339f)
    dict_copy = deepcopy(registration)
    if bool == True:
        embed=discord.Embed(title="Here are your Contacts", description="National Suicide Hotline: (800) 273-8255\n Attached are hotlines of UC's", color=0x1d339f)
    i = 0

    if ctx.author.id in list(dict_copy.keys()):
        del dict_copy[ctx.author.id]

    serious_contacts = [name for name in list(dict_copy.keys()) if dict_copy[name][len(dict_copy[name])-1] == True]

    while i < 3:
        if bool == True:
            if len(serious_contacts) == 0:
                i = 3
                break
            name = random.choice(serious_contacts)
        else:
            if len(dict_copy) == 0:
                i = 3
                break
            name = random.choice(list(dict_copy.keys()))

        if bool == True:
            embed.add_field(name=f"Discord: {dict_copy[name][0]}", value=f"Discord: {dict_copy[name][1]}", inline=True)
            i += 1
            serious_contacts.remove(name)
        else:
            embed.add_field(name=f"Discord: {dict_copy[name][0]}", value=f"Discord: {dict_copy[name][1]}", inline=True)
            i += 1
            del dict_copy[name]

    select = Select(placeholder="View Help Lines by UC", options=[
        discord.SelectOption(label = "UC Irvine", description = "(949) 824-6457", emoji="<:uciicon:977760745284591636>"),
        discord.SelectOption(label = "UC Berkeley", description = "(510) 642-9494", emoji="<:ucb:977761999670902794>"),
        discord.SelectOption(label = "UC Los Angeles", description = "(310) 825-0768", emoji="<:ucla:977762358971727882>"),
        discord.SelectOption(label = "UC Santa barbara", description = "(805) 893-4411", emoji="<:ucsb:977761572598468659>"),
        discord.SelectOption(label = "UC San Diego", description = "(858) 534-3755", emoji="<:ucsd:977762396384944160>"),
        discord.SelectOption(label = "UC Davis", description = "(916) 386-3620", emoji="<:ucd:977761785513902092>"),
        discord.SelectOption(label = "UC Santa Cruz", description = "(831) 459-2628", emoji="<:ucsc:977762553277059133>"),
        discord.SelectOption(label = "UC Riverside", description = "(951) 827-5531", emoji="<:ucr:977762334577680384>"),
        discord.SelectOption(label = "UC Merced", description = "(209) 228-4266", emoji="<:ucm:977762317750124594>"),
    ])
    view = View()
    view.add_item(select)
    if bool == True:
        await ctx.author.send(embed=embed, view=view)
    else:
        await ctx.author.send(embed=embed)

async def report(ctx, client):
    report_ids = [190936845914341377]
    info = await client.fetch_user(random.choice(report_ids))
    info2 = await client.fetch_user(ctx.author.id)
    
    embed=discord.Embed(title=f"{info2} has reported a misuse of the application", color=0x1d339f)
    await info.send(embed=embed)


async def completed(ctx):
    embed=discord.Embed(title="Operation Completed", color=0x1d339f)
    await ctx.author.send(embed=embed)

async def register(ctx, registration, client):
    embed=discord.Embed(title="Register", description="You are registering to make yourself available to making friends/source of cntact.  You will be inputting: [Optional Phone Number], [Whether you want to be available serious]", color=0x1d339f)

    reg1 = Button(label = "Continue", style=discord.ButtonStyle.green)
    reg2 = Button(label = "Quit", style=discord.ButtonStyle.red)

    async def reg1_i(interaction):
        await interaction.response.defer()
        reg2.disabled = True
        reg1.disabled = True
        await interaction.message.edit(view=regview)

        if ctx.author.id in list(registration.keys()):
            del registration[ctx.author.id]

        registration[ctx.author.id].append(str(ctx.author))

        embed=discord.Embed(title="Phone Number", description="Please Enter Your Phone Number (Type N/A if opt out)", color=0x1d339f)
        await ctx.author.send(embed=embed)
        phone = await client.wait_for('message', check=lambda message: message.author == ctx.author)
        registration[ctx.author.id].append(phone.content)
        print(registration[ctx.author.id][1])

        embed=discord.Embed(title="Serious Contact", description="Do you wish to be a serious contact?", color=0x1d339f)
        regyes = Button(label = "Yes", style=discord.ButtonStyle.green)
        regno = Button(label = "No", style=discord.ButtonStyle.red)

        async def regy(interaction):
            await interaction.response.defer()
            registration[ctx.author.id].append(True)
            await completed(ctx)
            regyes.disabled = True
            regno.disabled = True
            await interaction.message.edit(view=reg_ser)

        async def regn(interaction):
            await interaction.response.defer()
            registration[ctx.author.id].append(False)
            await completed(ctx)
            regyes.disabled = True
            regno.disabled = True
            await interaction.message.edit(view=reg_ser)

        regyes.callback = regy
        regno.callback = regn

        reg_ser = View()
        reg_ser.add_item(regyes)
        reg_ser.add_item(regno)
        
        await ctx.author.send(embed=embed, view=reg_ser)

    async def reg2_i(interaction):
        await interaction.response.defer()
        reg1.disabled = True
        reg2.disabled = True
        await interaction.message.edit(view=regview)

    reg1.callback = reg1_i
    reg2.callback = reg2_i
    regview = View()
    regview.add_item(reg1)
    regview.add_item(reg2)

    await ctx.author.send(embed=embed, view=regview)

async def serious(ctx, registration):
    embed=discord.Embed(title="Providing Contacts", description="Does this require serious contacts?", color=0x1d339f)
    regyes = Button(label = "Yes", style=discord.ButtonStyle.green)
    regno = Button(label = "No", style=discord.ButtonStyle.red)

    async def regy(interaction):
        await interaction.response.defer()
        regyes.disabled = True
        regno.disabled = True
        await interaction.message.edit(view=reg_ser)
        await send_names(ctx, registration, True)

    async def regn(interaction):
        await interaction.response.defer()
        regyes.disabled = True
        regno.disabled = True
        await interaction.message.edit(view=reg_ser)
        await send_names(ctx, registration, False)

    regyes.callback = regy
    regno.callback = regn

    reg_ser = View()
    reg_ser.add_item(regyes)
    reg_ser.add_item(regno)
    
    await ctx.author.send(embed=embed, view=reg_ser)

async def reg_remove(registration, ctx):
    if ctx.author.id in list(registration.keys()):
        del registration[ctx.author.id]
    embed=discord.Embed(title="Sucessfully Removed", description="", color=0x1FA31F)
    await ctx.author.send(embed=embed)

async def help_commands(ctx):
    introduction_description = """I'm a bot that's here for you and me ;) , whether that's making friends, finding someone to talk to, or just random, fun things. \
    I can do lots, like giving out random dog facts, sending a recipe to cook, or even telling you what the weather's like anywhere in the world, \
    just to name a few. Nice to meetcha :)"""
    embed1=discord.Embed(title="Hi! My name is Umi.", description=introduction_description, color=0xa23506)
    embed1.set_footer(text="page 1 of 4")

    embed2=discord.Embed(title="Contacts", description="Find Someone To Talk To!\n---Commands---", color=0xa23506)
    embed2.add_field(name="register", value="- register to be a contact that others can talk to.", inline=False)
    embed2.add_field(name="connect", value="- sign up to be connected to others.", inline=False)
    embed2.add_field(name="report", value="- report users that misuse/abuse this system.", inline=False)
    embed2.set_footer(text="page 2 of 4")

    embed3=discord.Embed(title="Daily Subscriptions! Try them out!", color=0xa23506)
    embed3.add_field(name="regdaily", value="- choosing subscription features", inline=False)
    embed3.add_field(name="mydaily", value="- displays personalized subscriptions", inline=False)
    embed3.add_field(name="dailyall", value="- displays all features", inline=False)
    embed3.add_field(name="activity", value="- random stuff to do when you're bored", inline=False)
    embed3.add_field(name="quote", value="- cheer up with an inspirational quote!", inline=False)
    embed3.add_field(name="recipe", value="- for when you're not sure what to make for dinner", inline=False)
    embed3.add_field(name="cat", value="- hehe cat facts. Cats are the cutest", inline=True)
    embed3.add_field(name="dog", value="- dog facts! Dogs r also the cutest", inline=False)
    embed3.add_field(name="dailydose", value="- a Daily Dose Of Internet video. perfect way to start your day!", inline=True)
    embed3.add_field(name="exercise", value="- 1, 2! 1, 2! C'mon you can do another set!", inline=False)
    embed3.set_footer(text="page 3 of 4")

    embed4=discord.Embed(title="Fun/Miscellaneous commands! Try them out!", color=0xa23506)
    embed4.add_field(name="weather", value="- check the weather anywhere in the world!", inline=False)
    embed4.add_field(name="image", value="- search for a random image related to a topic", inline=False)
    embed4.add_field(name="translate", value="- translate any language into English!", inline=False)
    embed4.add_field(name="covid", value="- view a tracker COVID-19 stats ", inline=False)
    embed4.set_footer(text="page 4 of 4")

    button1 = Button(label="<-", style=discord.ButtonStyle.green, disabled=True)
    button2 = Button(label="->", style=discord.ButtonStyle.green)

    button3 = Button(label="<-", style=discord.ButtonStyle.green)
    button4 = Button(label="->", style=discord.ButtonStyle.green)

    button5 = Button(label="<-", style=discord.ButtonStyle.green)
    button6 = Button(label="->", style=discord.ButtonStyle.green)

    button7 = Button(label="<-", style=discord.ButtonStyle.green)
    button8 = Button(label="->", style=discord.ButtonStyle.green, disabled=True)
        
    async def button2_callback(interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(embed=embed2, view=view2)


    button2.callback = button2_callback

    async def button3_callback(interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(embed=embed1, view=view1)

    button3.callback = button3_callback

    async def button4_callback(interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(embed=embed3, view=view3)

    button4.callback = button4_callback

    async def button5_callback(interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(embed=embed2, view=view2)

    button5.callback = button5_callback

    async def button6_callback(interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(embed=embed4, view=view4)

    button6.callback = button6_callback

    async def button7_callback(interaction):
        await interaction.response.defer()
        await interaction.edit_original_message(embed=embed3, view=view3)

    button7.callback = button7_callback

    view1 = View()
    view1.add_item(button1)
    view1.add_item(button2)

    view2 = View()
    view2.add_item(button3)
    view2.add_item(button4)

    view3 = View()
    view3.add_item(button5)
    view3.add_item(button6)

    view4 = View()
    view4.add_item(button7)
    view4.add_item(button8)

    await ctx.channel.send(embed=embed1, view=view1)

