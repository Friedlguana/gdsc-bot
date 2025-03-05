import asyncio
import datetime
from discord.ext import commands, tasks

reminders = []  # In-memory storage (can be swapped for database later)

class Reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cleanup_reminders.start()

    @commands.command(name="setreminder")
    async def set_reminder(self, ctx, date: str, time: str, *, message: str):
        try:
            date_time_str = f"{date} {time}"
            reminder_time = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")

            reminders.append({
                "time": reminder_time,
                "message": message,
                "user": ctx.author
            })

            await ctx.send(f"✅ Reminder set for **{date} at {time}**: {message}")
        except ValueError:
            await ctx.send("❌ Invalid format. Use: `YYYY-MM-DD HH:MM`")

    @commands.command(name="reminders")
    async def list_reminders(self, ctx):
        user_reminders = [r for r in reminders if r['user'] == ctx.author]

        if not user_reminders:
            await ctx.send("📭 You have no reminders set.")
        else:
            msg = "\n".join([f"{i+1}. 📅 **{r['time'].strftime('%Y-%m-%d %H:%M')}** - {r['message']}" 
                              for i, r in enumerate(user_reminders)])
            await ctx.send(f"📋 **Your Reminders:**\n{msg}")

    @commands.command(name="deletereminder")
    async def delete_reminder(self, ctx, index: int):
        user_reminders = [r for r in reminders if r['user'] == ctx.author]

        if index < 1 or index > len(user_reminders):
            await ctx.send("❌ Invalid reminder number.")
            return

        reminder = user_reminders[index - 1]
        reminders.remove(reminder)
        await ctx.send(f"✅ Deleted reminder: {reminder['message']}")

    @commands.command(name="modifyreminder")
    async def modify_reminder(self, ctx, index: int, date: str, time: str, *, new_message: str):
        user_reminders = [r for r in reminders if r['user'] == ctx.author]

        if index < 1 or index > len(user_reminders):
            await ctx.send("❌ Invalid reminder number.")
            return

        try:
            date_time_str = f"{date} {time}"
            new_time = datetime.datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")

            reminder = user_reminders[index - 1]
            reminder['time'] = new_time
            reminder['message'] = new_message

            await ctx.send(f"✅ Reminder updated to **{date} at {time}**: {new_message}")
        except ValueError:
            await ctx.send("❌ Invalid format. Use: `YYYY-MM-DD HH:MM`")

    @tasks.loop(seconds=60)
    async def cleanup_reminders(self):
        now = datetime.datetime.now()
        expired = [r for r in reminders if r['time'] <= now]

        for r in expired:
            try:
                await r['user'].send(f"⏰ Reminder: {r['message']}")
            except Exception as e:
                print(f"[WARN] Failed to DM user {r['user']}: {e}")
            reminders.remove(r)

    @cleanup_reminders.before_loop
    async def before_cleanup(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Reminder(bot))
