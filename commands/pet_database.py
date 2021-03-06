from discord.ext import commands
import dataset
import random
import discord
from settings import SQL_DATABASE

# Create a pet database for the server!

db = dataset.connect(SQL_DATABASE)
table = db["pets"]

def setup(bot):
    bot.add_cog(Add_Pet(bot))
    bot.add_cog(Delete_Pet(bot))
    bot.add_cog(Gen_Pet(bot))
    bot.add_cog(List_Pet(bot))
    bot.add_cog(Custom_Pet(bot))

class Add_Pet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def addpet(self, ctx, *args):
        """add your pet!\nusage: addpet <pet name> with an attachment,\nor addpet <pet name> <url>"""
        if len(args) == 0:
            await ctx.send("Please enter a name for your pet!")

        elif len(args) == 1:
            if len(ctx.message.attachments) != 0:
                try:
                    for image in ctx.message.attachments:
                        table.insert(dict(name=args[0].capitalize(), url=image.url, owner=ctx.author.id))
                    await ctx.send(f"Successfully added all images of {args[0].capitalize()} to the database!")
                except Exception as e:
                    await ctx.send("Something went wrong! Let eva know.")
                    raise e
            
            else:
                await ctx.send("Please attach a photo to this image!!!! My database breaks easily im a fragile being")
    
        elif len(args) == 2:
            try:
                table.insert(dict(name=args[0].capitalize(), url=args[1], owner=ctx.author.id))
                await ctx.send(f"Successfully added image of {args[0].capitalize()} to the database!")
            except Exception as e:
                await ctx.send("Something went wrong! Let eva know.")
                raise e

class Delete_Pet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def delpet(self, ctx, arg):
        """deletes a pet.\nusable only by eva, for now."""
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
        """generate a random image of a (optionally specific) pet.\nusage: pet, or pet <pet name>."""
        if len(args) == 0:
            random_urls = []

            for pet in table:
                random_urls.append(pet["url"])
            try:
                await ctx.send(embed=discord.Embed().set_image(url=random.choice(random_urls)))
            except:
                await ctx.send(random.choice(random_urls))
        
        elif len(args) > 0:
            random_urls = []
            
            for pet in table.find(name=args[0].capitalize()):
                random_urls.append(pet["url"])
            
            try:
                await ctx.send(embed=discord.Embed().set_image(url=random.choice(random_urls)))
            except:
                await ctx.send(random.choice(random_urls))

class List_Pet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def listpets(self, ctx):
        """lists all pets in mio's database."""
        pet_list = table.distinct("name", "owner")
        unique_pets = []

        for pet in pet_list:
            try:
                owner = ctx.guild.get_member(pet['owner'])
                unique_pets.append(str(f"{pet['name']} - owned by **{owner.name}#{owner.discriminator}**"))
            except:
                pass

        embed = discord.Embed(
            title="List of Pets",
            description="\n".join(unique_pets)
            )
        
        embed.set_footer(text="pets are beautiful")

        await ctx.send(embed=embed)

class Custom_Pet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.is_owner()
    async def custompet(self, ctx, arg1, arg2, arg3):
        """only usable by eva.\na manual method of adding a pet with custom database options."""
        try:
            table.insert(dict(name=arg1, url=arg2, owner=int(arg3)))
            await ctx.send(f"NAME: {arg1}\nURL: <{arg2}>\nOWNER ID: {arg3}")
        except Exception as e:
            await ctx.send("Something went wrong.")
            raise e