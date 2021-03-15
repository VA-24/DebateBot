import discord
from discord.ext import commands
import random
import datetime
import asyncio
import nltk
from nltk.stem import WordNetLemmatizer
import yfinance as yf
import datetime
from bs4 import BeautifulSoup
import requests
import datanews
import json
import csv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

players = {}


lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np

from keras.models import load_model

model = load_model('chatbot_model.h5')
import json
import random

intents = json.loads(open('debateintesnts.json').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return (np.array(bag))


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for tg in list_of_intents:
        if (tg['tag'] == tag):
            responses = random.choice(tg['responses'])
            break
    return responses


def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


"""
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)
"""

#DebateBot v1.3

client = commands.Bot(command_prefix = "d!")
client.remove_command('help')

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Yoink Simulator v3000"))
    print("Bot is ready. ")

@client.event
async def on_member_join(member):
    print(f'{member} has joined the server.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left the server.')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pong!')

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason=reason)

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason=reason)

@client.command()
async def createrole(ctx, *, role:str, fields=None):
    await ctx.guild.create_role(name = role, reason=None)

@client.command()
async def purge(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

@client.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)

    await member.add_roles(mutedRole, reason=reason)
    await ctx.send(f"Muted {member.mention} for reason {reason}")
    await member.send(f"You were muted in the server {guild.name} for {reason}")

@client.command()
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")

    await member.remove_roles(mutedRole)
    await ctx.send(f"Unmuted {member.mention}")
    await member.send(f"You were unmuted in the server {ctx.guild.name}")

@client.command()
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(

        title = "Commands (thus far)",
        description = "help commands",
        colour = discord.Colour.blue()
    )


    embed.add_field(name="d!stock <stock abbreviation>", value="Tells you the current stock price, as well as the change from yesterday's close", inline=False)
    embed.add_field(name="d!debatevid", value="Brings up a debatevid", inline=False)
    embed.add_field(name="d!newsarticle <query>", value="Retrieves a news article", inline=False)
    embed.add_field(name="d!rememberbirthday <user> <month> <day>", value="Tells the bot to remember your birthday. When giving a name, don't use @", inline=False)
    embed.add_field(name="d!birthdays", value="Shows all the server birthdays, in addition to the birthdays on that specific day", inline=False)
    embed.add_field(name="d!searchurban <query1 + query2>", value="Searches urban dictionary for a word that you tell the bot", inline=False)
    embed.add_field(name="d!8ball <query>", value="Returns a random answer for a question you ask", inline=False)
    embed.add_field(name="d!chat <prompt>", value="uses machine learning to respond to what you say", inline=False)
    embed.add_field(name="d!ping", value="Returns Pong!", inline=False)

    await ctx.send(embed=embed)


@client.command()
async def debatevid(ctx):
    debatevids = ['https://www.youtube.com/watch?v=_XU92LHHk2Y&list=PLHaG-zIzA-QFVlMUHD2LO30Lz1R2kt1hn', 'https://www.youtube.com/watch?v=u5C1SIiQZ6I&list=PLHaG-zIzA-QFVlMUHD2LO30Lz1R2kt1hn&index=2', 'https://www.youtube.com/watch?v=56G8OyvSxk0&list=PLHaG-zIzA-QFVlMUHD2LO30Lz1R2kt1hn&index=3', 'https://www.youtube.com/watch?v=LrTYHn1Am0c&list=PLHaG-zIzA-QFVlMUHD2LO30Lz1R2kt1hn&index=4', 'youtube.com/watch?v=rsFoizOHVFg&list=PLHaG-zIzA-QFVlMUHD2LO30Lz1R2kt1hn&index=5', 'https://www.youtube.com/watch?v=31AFA6HJThc&list=PLHaG-zIzA-QFVlMUHD2LO30Lz1R2kt1hn&index=6', 'https://www.youtube.com/watch?v=US-pxWceS0E&list=PLHaG-zIzA-QFVlMUHD2LO30Lz1R2kt1hn&index=7', 'https://www.youtube.com/watch?v=oYfCvuekHeY&list=PLHaG-zIzA-QFVlMUHD2LO30Lz1R2kt1hn&index=8', 'https://www.youtube.com/watch?v=16kQiCxa6ao&list=PLHaG-zIzA-QFVlMUHD2LO30Lz1R2kt1hn&index=9', 'https://www.youtube.com/watch?v=QVijCuyirKw&list=PLHaG-zIzA-QFVlMUHD2LO30Lz1R2kt1hn&index=10', 'https://www.youtube.com/watch?v=AVM-Y9Np3SM&list=PLHaG-zIzA-QFVlMUHD2LO30Lz1R2kt1hn&index=11', 'https://www.youtube.com/watch?v=wMRhPz2PZ3M&list=PLHaG-zIzA-QFVlMUHD2LO30Lz1R2kt1hn&index=12']
    await ctx.send(f'{random.choice(debatevids)}')

@client.command()
async def rememberbirthday(ctx, member, month, day):
    with open('birthdays.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([member, f'{month}', f'{day}'])
    await ctx.send("Stored data!")

@client.command()
async def birthdays(ctx):
    tag_list = []
    month_list = []
    day_list = []

    with open("birthdays.csv", "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            day_list.append(row[2])
            month_list.append(row[1])
            tag_list.append(row[0])

    embed = discord.Embed(

        title="Server Birthdays",
        description=":D",
        colour=discord.Colour.blue()
    )


    for i in range(len(tag_list)):
        embed.add_field(name=str(tag_list[i]), value=str(month_list[i]) + "/" + str(day_list[i]), inline=False)

    await ctx.send(embed=embed)

    today = datetime.date.today()

    for i in range(len(tag_list)):
        if (int(month_list[i]) == int(today.month)):
            if (int(day_list[i]) == int(today.day)):
                await ctx.send("hbd " + str(tag_list[i]))

"""
@client.command()
async def debatersummary(ctx, debater):
    driver.get('https://www.debatestat.com/ind/')

    search = driver.find_element_by_id('dInput')
    search.send_keys(f'{debater}')
    search.send_keys(Keys.RETURN)

    time.sleep(3)

    driver.save_screenshot(f'{debater}.png')

    await ctx.channel.send(file=discord.File(f'{debater}.png'))
"""

@client.command()
async def w(ctx, member):
    await ctx.send(f'{member} won their round!')

@client.command()
async def l(ctx, member):
    await ctx.send(f'{member} lost their round.')

@client.command()
async def gayrate(ctx, member):
    await ctx.send(f'{member} is ' + str(random.randrange(100)) + "% gay")

@client.command()
async def gangsta(ctx, member):
    await ctx.send(f'{member} is ' + str(random.randrange(100)) + "% Gangsta")

@client.command()
async def Dlength(ctx, member):

    if 'noswad' in str(member):
        await ctx.send('Noswad has an immeasurable D, and he is clearly the alpha')
    elif 'ultraman' in str(member):
        await ctx.send('8===============================================================D')
    else:
        await ctx.send(f'{member} has a length ' + '8' + '=' * random.randrange(15) + 'D')

@client.command()
async def chat(ctx, *, question):
    msg = question

    if msg != '':
        await ctx.send(f'You: {question}')
        res = chatbot_response(msg)
        await ctx.send(f'Bot: {res}')

@client.command(pass_context=True)
async def quickpoll(ctx, question, *options: str):
    channel = client.get_channel(805631885127581726)

    if len(options) <= 1:
        await client.say('You need more than one option to make a poll!')
        return
    if len(options) > 5:
        await client.say('You cannot make a poll for more than 5 things!')
        return

    if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
        reactions = ['✅', '❌']
    elif len(options) == 3:
        reactions = ['1️⃣','2️⃣','3️⃣']
    elif len(options) == 4:
        reactions = ['1️⃣','2️⃣','3️⃣','5️⃣']
    else:
        reactions = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣']

    description = []
    for x, option in enumerate(options):
        description += '\n {} {}'.format(reactions[x], option)
    embed = discord.Embed(title=question, description=''.join(description))
    react_message = await channel.send(embed=embed)

    embed.set_footer(text='Poll ID: {}'.format(react_message.id))
    await client.edit_message(react_message, embed=embed)


@client.command()
async def searchurban(ctx, word):
    word_len = len(word.split())
    word_replace = word.replace(" ", "+")
    if word_len > 1:
        await ctx.send('https://www.urbandictionary.com/define.php?term=' + word_replace)
    else:
        await ctx.send('https://www.urbandictionary.com/define.php?term=' + word)

@client.command()
async def newsarticle(ctx, keyword):
    try:
        datanews.api_key = '0dpjcz61674lclqogfkxhsyhx'

        response = datanews.headlines(q=f'{keyword}', language=['en'])
        articles = response['hits']
        await ctx.send(articles[random.randrange(0,10)]['url'])
    except:
        await ctx.send('Sorry! It looks like there are no current events that match your query. Try a wikisearch instead')

@client.command()
async def wikisearch(ctx, keyword):
    try:
        await ctx.send(f'https://en.wikipedia.org/wiki/{keyword}')
    except:
        await ctx.send("Sorry! That wiki article doesn't exist (L)")


@client.command()
async def stock(ctx, tickersymbol, time):

    if time == 'week':
        tickerdata = yf.Ticker(tickersymbol)
        tickerinfo = tickerdata.info
        investment = tickerinfo['shortName']
        await ctx.send(investment)

        today = datetime.date.today()

        date = str(today.year) + "-" + str(today.month) + "-" + str(today.day)

        tickerDF = tickerdata.history(period='5d', start='2020-1-1')
        priceLast = tickerDF['Close'].iloc[-1]
        priceYest = tickerDF['Close'].iloc[-2]
        pctdiff = round(((priceLast-priceYest)/priceYest)*100, 2)
        await ctx.send(priceLast)
        if pctdiff < 0:
            await ctx.send(f'{investment} is down {pctdiff} percent from last 5d period')
        else:
            await ctx.send(f'{investment} is up {pctdiff} percent from last 5d period')
    if time == 'day':
        tickerdata = yf.Ticker(tickersymbol)
        tickerinfo = tickerdata.info
        investment = tickerinfo['shortName']
        await ctx.send(investment)

        today = datetime.date.today()

        date = str(today.year) + "-" + str(today.month) + "-" + str(today.day)

        tickerDF = tickerdata.history(period='1d', start='2020-1-1', end=date)
        priceLast = tickerDF['Close'].iloc[-1]
        priceYest = tickerDF['Close'].iloc[-2]
        pctdiff = round(((priceLast-priceYest)/priceYest)*100, 2)
        await ctx.send(priceLast)
        if pctdiff < 0:
            await ctx.send(f'{investment} is down {pctdiff} percent from yesterday')
        else:
            await ctx.send(f'{investment} is up {pctdiff} percent from yesterday')
    if time == 'month':
        tickerdata = yf.Ticker(tickersymbol)
        tickerinfo = tickerdata.info
        investment = tickerinfo['shortName']
        await ctx.send(investment)

        today = datetime.date.today()

        date = str(today.year) + "-" + str(today.month) + "-" + str(today.day)

        tickerDF = tickerdata.history(period='1mo', start='2020-1-1')
        priceLast = tickerDF['Close'].iloc[-1]
        priceYest = tickerDF['Close'].iloc[-2]
        pctdiff = round(((priceLast-priceYest)/priceYest)*100, 2)
        await ctx.send(priceLast)
        if pctdiff < 0:
            await ctx.send(f'{investment} is down {pctdiff} percent from the close of last month')
        else:
            await ctx.send(f'{investment} is up {pctdiff} percent from the close of last month')
    if time == 'quarter':
        tickerdata = yf.Ticker(tickersymbol)
        tickerinfo = tickerdata.info
        investment = tickerinfo['shortName']
        await ctx.send(investment)

        today = datetime.date.today()

        date = str(today.year) + "-" + str(today.month) + "-" + str(today.day)

        tickerDF = tickerdata.history(period='3mo', start='2020-1-1')
        priceLast = tickerDF['Close'].iloc[-1]
        priceYest = tickerDF['Close'].iloc[-2]
        pctdiff = round(((priceLast-priceYest)/priceYest)*100, 2)
        await ctx.send(priceLast)
        if pctdiff < 0:
            await ctx.send(f'{investment} is down {pctdiff} percent from the close of last quarter')
        else:
            await ctx.send(f'{investment} is up {pctdiff} percent from the close of last quarter')


@client.command(aliases = ["8ball"])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes – definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]

    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@client.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == 820769253569462303:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        if payload.emoji.name == 'dyang':
            role = discord.utils.get(guild.roles, name='Owner')
        elif payload.emoji.name == 'gtav':
            role = discord.utils.get(guild.roles, name='gtav')
        elif payload.emoji.name == 'cod':
            role = discord.utils.get(guild.roles, name='cod')
        elif payload.emoji.name == 'LoL':
            role = discord.utils.get(guild.roles, name='LoL')
        elif payload.emoji.name == 'csgo':
            role = discord.utils.get(guild.roles, name='csgo')

        #you're not just limited to these games, you can also add other ones
        #make sure that you have appropriate custom emojis as well as role names
        #you can create rolenames using g!createrole <rolename here>
        #(you also dont have to create just gaming roles)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
                print("done")

client.run('token')
