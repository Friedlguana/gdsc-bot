import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import asyncio
import shutil

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_client = None
        self.current_song = None
        self.queue = asyncio.Queue()
        self.playing = False

        # Automatically detect ffmpeg location
        self.ffmpeg_path = shutil.which("ffmpeg")
        if not self.ffmpeg_path:
            raise RuntimeError("❌ `ffmpeg` not found! Make sure it's installed and added to PATH.")

    async def ensure_voice(self, ctx):
        """Ensure the bot is connected to VC. Auto-joins if needed."""
        if ctx.voice_client and ctx.voice_client.is_connected():
            return True  # Already in VC

        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("❌ You need to **join a voice channel** first.")
            return False

        channel = ctx.author.voice.channel
        print(f"[DEBUG] Joining VC: {channel.name}")

        try:
            self.voice_client = await channel.connect()
            await ctx.send(f"✅ Joined **{channel.name}**")
            return True
        except Exception as e:
            await ctx.send(f"❌ Failed to join VC: `{e}`")
            print(f"[ERROR] Failed to join VC: {e}")
            return False

    async def play_next(self, ctx):
        """Play the next song in the queue if available."""
        if self.queue.empty():
            self.playing = False
            await ctx.send("✅ Queue ended.")
            return

        song = await self.queue.get()
        await self.play_song(ctx, song['url'], song['title'])

    async def play_song(self, ctx, url, title):
        """Handles actually playing a song with FFmpeg."""
        self.current_song = title
        self.playing = True

        ffmpeg_opts = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }

        source = discord.FFmpegOpusAudio(url, executable=self.ffmpeg_path, **ffmpeg_opts)

        def after_playing(error):
            if error:
                print(f"[ERROR] Playback error: {error}")
            asyncio.run_coroutine_threadsafe(self.play_next(ctx), self.bot.loop)

        ctx.voice_client.play(source, after=after_playing)
        await ctx.send(f"🎶 Now playing: **{title}**")

    async def get_song_info(self, query):
        """Fetch song info from YouTube."""
        ytdl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'extractaudio': True,
            'noplaylist': True,
            'default_search': 'ytsearch',
            'force-ipv4': True
        }

        loop = asyncio.get_event_loop()
        with youtube_dl.YoutubeDL(ytdl_opts) as ytdl:
            info = await loop.run_in_executor(None, lambda: ytdl.extract_info(query, download=False))
            if 'entries' in info:
                info = info['entries'][0]
        return info

    @commands.command(name="play")
    async def play(self, ctx, *, query: str):
        """Searches YouTube, joins VC (if needed), and plays/queues the song."""
        if not await self.ensure_voice(ctx):
            return

        info = await self.get_song_info(query)
        title, url = info['title'], info['url']

        await ctx.send(f"🔎 Found: **{title}**")

        if self.playing or ctx.voice_client.is_playing():
            await self.queue.put({'title': title, 'url': url})
            await ctx.send(f"➕ Added to queue: **{title}**")
        else:
            await self.play_song(ctx, url, title)

    @commands.command(name="queue")
    async def show_queue(self, ctx):
        """Displays the queue."""
        if self.queue.empty():
            await ctx.send("📭 Queue is empty.")
        else:
            upcoming = list(self.queue._queue)
            queue_list = "\n".join([f"• {song['title']}" for song in upcoming])
            await ctx.send(f"📜 Current Queue:\n{queue_list}")

    @commands.command(name="skip")
    async def skip(self, ctx):
        """Skips the current song."""
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            await ctx.send("❌ No song is playing.")
            return

        ctx.voice_client.stop()
        await ctx.send("⏭ Skipped!")

    @commands.command(name="stop")
    async def stop(self, ctx):
        """Stops playback and clears the queue."""
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            await ctx.send("❌ No song is playing.")
            return

        self.queue = asyncio.Queue()  # Clear queue
        ctx.voice_client.stop()
        await ctx.send("⏹ Stopped playback and cleared queue.")

    @commands.command(name="leave")
    async def leave(self, ctx):
        """Leaves the voice channel and clears the queue."""
        if ctx.voice_client and ctx.voice_client.is_connected():
            self.queue = asyncio.Queue()
            await ctx.voice_client.disconnect()
            self.voice_client = None
            self.playing = False
            await ctx.send("👋 Left the voice channel.")
        else:
            await ctx.send("❌ I'm not in a voice channel.")

async def setup(bot):
    await bot.add_cog(Music(bot))
