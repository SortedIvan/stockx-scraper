from math import prod
import discord
from main import scrapeProductInformation

token = "MTAxNDU2NjUwNDA5NzkyMzE0Mg.Gb3eE_.Hg2ipgO2Op60HAAFhHg8NukFE6Zp26ZhHRGX2g"

client = discord.Client(intents=discord.Intents.default())


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.split(' ')[0] == '!stockxquery':
        query = message.content.replace('!stockxquery', '')
        product = scrapeProductInformation(query)

    embed = discord.Embed(
        title = "HI"
    )
    embed = discord.Embed(
        title=product['title'],
        url = "https://stockx.com/en-gb/" + product['urlKey']
    )

    embed.set_thumbnail(
        url = product['media']['imageUrl']
    )
    embed.add_field(
        name = "Has asks",
        value = f"{product['market']['hasAsks']}"
    )
    embed.add_field(
        name = "Lowest ask & lowest ask size",
        value = f"Lowest ask: {product['market']['lowestAsk']} | Lowest ask size {product['market']['lowestAskSize']}"
    )

    embed.add_field(
        name = "Last sale & sale size",
        value = f"Sale: {product['market']['lastSale']} | Last sale size: {product['market']['lastSaleSize']}"
    )
    await message.channel.send(embed=embed)



client.run(token)