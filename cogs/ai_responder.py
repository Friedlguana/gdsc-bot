import discord
from discord.ext import commands
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_TOKEN")

genai.configure(api_key=GEMINI_API_KEY)

# Configure the correct model and generation settings
model = genai.GenerativeModel(model_name="gemini-1.5-pro", generation_config={"temperature": 0.5})

class AIResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ask")
    async def ask_ai(self, ctx, *, question: str):
        """Ask Gemini a direct question."""
        try:
            response = model.generate_content(question)
            await ctx.send(response.text)
        except Exception as e:
            await ctx.send(f"❌ Error fetching response: {e}")

    @commands.command(name="summarize")
    async def summarize(self, ctx, *, content: str):
        """Ask Gemini to summarize a given block of text."""
        try:
            prompt = f"Please summarize the following text:\n\n{content}"
            response = model.generate_content(prompt)
            await ctx.send(f"📝 Summary:\n{response.text}")
        except Exception as e:
            await ctx.send(f"❌ Error fetching summary: {e}")

async def setup(bot):
    await bot.add_cog(AIResponder(bot))
