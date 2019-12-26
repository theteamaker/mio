from discord.ext import commands
import dataset
import random
import discord

# Create a pet database for the server!

db = dataset.connect('sqlite:///database.db')
table = db["pets"]

class Add_Pet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def addpet(self, ctx, arg):
        try:
            for image in ctx.message.attachments:
                table.insert(dict(name=arg.capitalize(), url=image.url, owner=ctx.author.id))
            await ctx.send(f"Successfully added all images of {arg.capitalize()} to the database!")
        except Exception as e:
            await ctx.send("Something went wrong! Let eva know.")
            raise e

class Delete_Pet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def delpet(self, ctx, arg):
        try:
            table.delete(url=arg)
            await ctx.send("Successfully (and unfortunately) deleted a pet.")

        except Exception as e:
            await ctx.send("Something went wrong! Maybe the URL doesn't exist in the database.")
            raise e

class Gen_Pet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def pet(self, ctx, *args):
        if len(args) == 0:
            random_urls = []

            for pet in table:
                random_urls.append(pet["url"])
            
            await ctx.send(random.choice(random_urls))
        
        elif len(args) > 0:
            random_urls = []
            
            for pet in table.find(name=args[0].capitalize()):
                random_urls.append(pet["url"])
            
            await ctx.send(random.choice(random_urls))

class List_Pet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def listpets(self, ctx):
        pet_list = table.distinct("name", "owner")
        unique_pets = []

        for pet in pet_list:
            owner = ctx.guild.get_member(pet['owner'])
            unique_pets.append(str(f"{pet['name']} - owned by **{owner.name}#{owner.discriminator}**"))
        
        embed = discord.Embed(
            title="List of Pets",
            description="\n".join(unique_pets)
            )
        
        embed.set_footer(text="pets are beautiful")

        await ctx.send(embed=embed)