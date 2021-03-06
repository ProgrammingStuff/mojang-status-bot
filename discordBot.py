import discord, urllib.request, json, asyncio
from values import values, responses
 
client = discord.Client()
prefix = values["prefix"]
 
@client.event
async def on_message(message):
    if message.author ==  client.user:
        return
    strippedMessage = message.content.lower().split(prefix)[1]
    if message.content.startswith(prefix + 'status'):
        status = api_status()
        result = "----------------------------------------\n"
        laps = 0
        while laps < len(status):
            state = status[laps][1]
            if state == "green":
                state = ":white_check_mark:"
            elif state == "yellow":
                state = ":warning:"
            else:
                state = ":x:"
 
            if laps == 0:
                service = "Minecraft.net: "
            elif laps == 1:
                service = "Session: "
            elif laps == 2:
                service = "Mojang accounts website:   "
            elif laps == 3:
                service = "Authentication server: "
            elif laps == 4:
                service = "Sessions server: "
            elif laps == 5:
                service = "Public API: "
            elif laps == 6:
                service = "Minecraft textures: "
            else:
                service = "Mojang website: "
             
            formatted = service + "\n" + state.rjust(75)
            result = result + formatted + "\n" + "----------------------------------------" + "\n"
            laps = laps + 1
        await client.send_message(message.channel, result)
         
    elif strippedMessage in responses:
        await client.send_message(message.channel, responses[strippedMessage])
                                  
@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name= "Try " + prefix + "help || GLHF!"))
    print('Bot Running')
    print('--------------')
     
def api_status():
    """
    Returns a list with the status of various Mojang services.
    """
 
    url = "https://status.mojang.com/check"
    request = urllib.request.Request(url)
 
    opened = urllib.request.urlopen(request).read()
    load = json.loads(opened.decode("utf-8"))
 
    item_list = []
 
    for item in load:
        for key, value in item.items():
            item_list.append([key, value])
 
    return item_list
 
client.run(values["token"])
