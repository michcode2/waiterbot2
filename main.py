import discord
import discordtoken#module that has my client secret so this looks better


client = discord.Client()


#read the list of games on games.txt and put them in a list
games=[]
votes=[]
with open("games.txt","r") as file:
    for line in file:
        games.append(line.rstrip())#adds each line of the file, and gets rid of the \n at the end to make the rest of it simpler
        votes.append(0)

#says when the bot is ready
@client.event
async def on_ready():
    print('bot online')

#testing method
@client.event
async def on_message(message):
    if message.content.startswith('go'): #only respont if people use the keyword, makes testing easier
        channel=message.channel
        for i in range(len(games)):#for every game, send a message and add a reaction to each of them
            msg = await channel.send(games[i])
            await msg.add_reaction('\N{thumbs up sign}')


#when an emoji is added, change the list of votes
@client.event
async def on_reaction_add(reac,user):
    if user != client.user:#checking that the person adding reactions isn't the bot
        if reac.message.author.bot:#checking that the message is from the bot
            if reac.message.content in games:#checking that the message is one of the games
                index=games.index(reac.message.content)#finding where in the list the game is
                votes[index]=votes[index]+1#adding to the votes
        print(votes)

        
#does the same as above, but for when people remove reactions, not working yet
async def on_reaction_remove(reac,user):
    print("reaction removed")
    if user != client.user:
        if reac.message.author.bot:
            if reac.message.content in games:
                index=games.index(reac.message.content)
                votes[index]=votes[index]-1
        print(votes)


client.run(discordtoken.getToken())
