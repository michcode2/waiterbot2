import discord
import discordtoken#module that has my client secret so this looks better
import asyncio


client = discord.Client()


#read the list of games on games.txt and put them in a list
games=[]
votes=[]
with open("games.txt","r") as file:
    for line in file:
        games.append(line.rstrip())#adds each line of the file, and gets rid of the \n at the end to make the rest of it simpler
        votes.append(0)
        


async def tallyResults(channel):#checks the results
    temp=votes#temporary list to sort
    temp.sort(reverse=True)#have it go from 1,-4,5,2 to 5,2,1,-4
    i=0
    noTie=True
    while temp[i]==temp[i+1]:#if there are two indicies that are the same, there is a tie. If i gets high enough, there are no more data
        if i!=2:
            i=i+1
        else:
            break
        noTie=False

    if noTie:
        index=temp.index(temp[0])#check which game has won and say it
        await channel.send(games[index]+" has won.")
    else:#say there is a tie
        await channel.send("There is a "+str(i+1)+"-way tie.") 
    

#says when the bot is ready
@client.event
async def on_ready():
    print('bot online')

#testing method
@client.event
async def on_message(message):
    if message.content == 'go': #only respont if people use the keyword, makes testing easier
        channel=message.channel
        await channel.send("From now you have 60 seconds to vote. Good luck.")
        messages=[]
        for i in range(len(games)):#for every game, send a message and add a reaction to each of them
            msg = await channel.send(games[i])
            await msg.add_reaction('\N{thumbs up sign}')
            await msg.add_reaction('\N{thumbs down sign}')
            messages.append(msg)
        await asyncio.sleep(30)
        await channel.send("Voting is now over. Votes cast from now on will not be counted")

        await tallyResults(channel)


#when an emoji is added, change the list of votes
@client.event
async def on_reaction_add(reac,user):
    if user != client.user:#checking that the person adding reactions isn't the bot
        if reac.emoji == '\N{thumbs up sign}' or reac.emoji=='\N{thumbs down sign}':#only do the next bit if its the right emojis
            content=reac.message.content
            index=games.index(content)#finds where in votes the net vote should go


            net=0
            for reaction in reac.message.reactions:#loops over each reaction to the message 
                
                if reaction.emoji == '\N{thumbs up sign}':#if the reaction is a thumbs up, increase the net vote
                    net = net + reaction.count
                if reaction.emoji == '\N{thumbs down sign}':#if the reaction is a thumbs down, decrease the net vote
                    net = net - reaction.count
            
            votes[index]=net # store the result
            print(votes)


client.run(discordtoken.getToken())
