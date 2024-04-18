import discord
from decouple import config
import asyncio
import yt_dlp
from random import shuffle

def run_bot():
    try:
        TOKEN = config('DISCORD_TOKEN') # Get Discord token from environment variables
    except KeyError:
        print("Error: Discord token not found in environment variables.")
        return
    
    intents = discord.Intents.default()
    intents.message_content = True  # Enable intent to receive message content
    client = discord.Client(intents=intents)

    voice_clients = {}  # Dictionary to manage voice clients per server
    queues = {}  # Dictionary to manage song queues per server
    yt_dl_options = {
        "format": "bestaudio/best"
    }  # yt-dlp configuration to get the best audio quality
    ytdl = yt_dlp.YoutubeDL(yt_dl_options)

    # FFmpeg options for audio playback
    ffmpeg_options = {
        'before_options':
        '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn -filter:a "volume=0.25"'
    }

    def play_next_song(guild_id):
        if guild_id in queues and queues[guild_id]:
            if voice_clients[guild_id].is_playing():
                return
            song = queues[guild_id].pop(0)
            player = discord.FFmpegOpusAudio(song['url'], **ffmpeg_options)
            voice_clients[guild_id].play(player,
                                        after=lambda e: play_next_song(guild_id))
        else:
            asyncio.run_coroutine_threadsafe(voice_clients[guild_id].disconnect(),
                                            client.loop)

    @client.event
    async def on_ready():
        print(f'{client.user} is now online and ready for music')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        guild_id = message.guild.id

        if message.content.startswith("y!help"):
            help_message = (
                "🎵 **Music Bot Commands** 🎵\n"
                "- `y!play [URL]`: Add audio from the YouTube link to the playback queue.\n"
                "- `y!pause`: Pause the current audio.\n"
                "- `y!resume`: Resume paused audio.\n"
                "- `y!stop`: Stop the audio and disconnect the bot from the voice channel.\n"
                "- `y!queue`: Show the songs in the queue.\n"
                "- `y!skip`: Skip the current song.\n"
                "- `y!clear`: Clear the queue of songs.\n"
                "- `y!shuffle`: Shuffle the queue of songs randomly.\n"
                "- `y!help`: Show this help message.\n")
            await message.channel.send(help_message)

        elif message.content.startswith("y!play"):
            # Check if the user is in a voice channel
            if message.author.voice:
                voice_channel = message.author.voice.channel
                if guild_id not in voice_clients or not voice_clients[
                    guild_id].is_connected():
                    try:
                        voice_clients[guild_id] = await voice_channel.connect(self_deaf=True)
                    except discord.ClientException:
                        await message.channel.send("Failed to connect to voice channel.")
                        return
                url = message.content.split()[1]
                try:
                    data = await asyncio.get_event_loop().run_in_executor(
                        None, lambda: ytdl.extract_info(url, download=False))
                except Exception as e:
                    await message.channel.send(f"Error: {e}")
                    return
                song = {'title': data.get('title'), 'url': data.get('url')}
                if guild_id not in queues:
                    queues[guild_id] = []
                queues[guild_id].append(song)

                # Always send the message when a song is added to the queue
                await message.channel.send(
                    f"🎶 Song added to queue: {song['title']}")

                # If not playing, start playback
                if not voice_clients[guild_id].is_playing():
                    play_next_song(guild_id)
            else:
                await message.channel.send(
                    "You must be in a voice channel to use this command.")
        elif message.content.startswith("y!pause"):
            if guild_id in queues and voice_clients[guild_id].is_playing():
                voice_clients[guild_id].pause()
                await message.channel.send("⏸️ Song paused.")
            else:
                await message.channel.send("No songs playing to pause.")

        elif message.content.startswith("y!resume"):
            if guild_id in voice_clients and voice_clients[guild_id].is_connected():
                voice_clients[guild_id].resume()
                await message.channel.send("▶️ Playback resumed.")
            else:
                await message.channel.send("No paused playback to resume.")

        elif message.content.startswith("y!stop"):
            if guild_id in voice_clients and voice_clients[guild_id].is_connected():
                voice_clients[guild_id].stop()
                await voice_clients[guild_id].disconnect()
                await message.channel.send("⏹️ Playback stopped and bot disconnected.")
                # Clear the song queue
                queues[guild_id] = []
            else:
                await message.channel.send("No playback to stop.")

        elif message.content.startswith("y!queue"):
            queue_message = "🎶 **Playback Queue** 🎶\n"
            queue_message += "\n".join([
                f"{idx + 1}. {song['title']}"
                for idx, song in enumerate(queues.get(guild_id, []))
            ])
            await message.channel.send(
                queue_message if queue_message else "No songs in queue.")

        elif message.content.startswith("y!skip"):
            if guild_id in queues and voice_clients[guild_id].is_playing():
                voice_clients[guild_id].stop()
                await message.channel.send("⏩ Song skipped.")
            else:
                await message.channel.send("No songs playing to skip.")

        elif message.content.startswith("y!clear"):
            queues[guild_id] = []
            await message.channel.send("🗑️ Song queue cleared.")

        elif message.content.startswith("y!shuffle"):
            if guild_id in queues:
                shuffle(queues[guild_id])
                await message.channel.send("🔀 Song queue shuffled.")

    client.run(TOKEN)

run_bot()
