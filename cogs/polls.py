import discord
from discord.ext import commands

class Polls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="poll")
    async def create_poll(self, ctx, question: str, *options: str):
        if len(options) < 2:
            await ctx.send("Please provide at least two options.")
            return
        
        embed = discord.Embed(title=f"Poll: {question}", color=discord.Color.blue())
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

        for idx, option in enumerate(options[:5]):
            embed.add_field(name=f"{reactions[idx]} {option}", value="\u200b", inline=False)

        message = await ctx.send(embed=embed)
        for emoji in reactions[:len(options)]:
            await message.add_reaction(emoji)

async def setup(bot):
    await bot.add_cog(Polls(bot))
