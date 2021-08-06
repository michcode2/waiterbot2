import discord
import discordtoken#module that has my client secret so this looks better
import asyncio

client = discord.Client()



games=[]#list for games and their votes
votes=[]
dGames=[]#list for desserts and their votes
dVotes=[]

with open("games.txt","r") as file:
    for line in file:
        games.append(line.rstrip())#adds each line of the file, and gets rid of the \n at the end to make the rest of it simpler
        votes.append(0)

with open("desserts.txt","r") as file:#same as above
    for line in file:
        dGames.append(line.rstrip())
        dVotes.append(0)
        




async def tallyResults(msgs,mains):#checks the results, with a bool for wether or not to use the mains set of lists
    channel=msgs[0].channel#useful for sending messages
    i=0
    for game in msgs:
        #goes over all the reactions on each message, and if they are thumbs ups/downs, the right number will be added to the overal votes. the bots votes will cancel out
        net=0
        for reaction in game.reactions:
            
            if reaction.emoji == '\N{thumbs up sign}':#if the reaction is a thumbs up, increase the net vote
                net = net + reaction.count
            if reaction.emoji == '\N{thumbs down sign}':#if the reaction is a thumbs down, decrease the net vote
                net = net - reaction.count
            if mains:#if mains: here and in the rest of the function sets/gets the right information from the right array, so this function can work for mains and desserts
                votes[i]=net # store the result
            else:
                dVotes[i]=net
            
        i=i+1
    if mains:
        temp=votes#temporary list to sort
    else:
        temp=dVotes
    temp.sort(reverse=True)#have it go from 1,-4,5,2 to 5,2,1,-4
    i=0
    noTie=True
    while temp[i]==temp[i+1]:#if there are two indicies that are the same, there is a tie. If i gets high enough, there are no more data
        if i!=len(temp)-2:
            i=i+1
        else:
            break
        noTie=False

    if noTie:
        index=temp.index(temp[0])#check which game has won and say it
        if mains:
            await channel.send(games[index]+" has won.")
        else:
            await channel.send(dGames[index]+" has won.")
    else:#say there is a tie
        await channel.send("There is a tie.") 
    

#says when the bot is ready
@client.event
async def on_ready():
    print('bot online')
        
        
#testing method
@client.event
async def on_message(message):
    if message.content.startswith("/wbm"): #only respond if people use the keyword, makes testing easier
        
        if message.content[5:]=="mains":
            channel=message.channel
            await channel.send("@everyone from now you have 2 minutes to vote on a main course. Good luck.")
            messages=[]
            for i in range(len(games)):#for every game, send a message and add a reaction to each of them. Finally adds them to a list for the tallying method
                msg = await channel.send(games[i])
                await msg.add_reaction('\N{thumbs up sign}')
                await msg.add_reaction('\N{thumbs down sign}')
                messages.append(discord.utils.get(client.cached_messages,id=msg.id))
            await asyncio.sleep(120)#wait a bit then tally the results
            await channel.send("Voting is now over. Votes cast from now on will not be counted")
            
            
            await tallyResults(messages,True)
            
        elif message.content[5:]=="dessert":#same as above but for mains
            channel=message.channel
            await channel.send("@everyone from now you have 2 minutes to vote on a dessert. Good luck.")
            messages=[]
            for i in range(len(dGames)):
                msg = await channel.send(dGames[i])
                await msg.add_reaction('\N{thumbs up sign}')
                await msg.add_reaction('\N{thumbs down sign}')
                messages.append(discord.utils.get(client.cached_messages,id=msg.id))
            await asyncio.sleep(120)
            await channel.send("Voting is now over. Votes cast from now on will not be counted")
            
            
            await tallyResults(messages,False)



client.run(discordtoken.getToken())
