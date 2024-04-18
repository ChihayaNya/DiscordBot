# Discord Music Bot 🎵

This Discord bot allows users to play music from YouTube in voice channels. It supports various commands to manage the playback queue and control audio playback.

---

## Features 🚀

- Play music from YouTube by providing the URL
- Pause and resume playback
- Stop playback and disconnect the bot from the voice channel
- View the current playback queue
- Skip the current song
- Clear the playback queue
- Shuffle the playback queue randomly
- Help command to display available commands

---

## Commands 🔧

- `y!play [URL]`: Add audio from the YouTube link to the playback queue.
- `y!pause`: Pause the current audio.
- `y!resume`: Resume paused audio.
- `y!stop`: Stop the audio and disconnect the bot from the voice channel.
- `y!queue`: Show the songs in the queue.
- `y!skip`: Skip the current song.
- `y!clear`: Clear the queue of songs.
- `y!shuffle`: Shuffle the queue of songs randomly.
- `y!help`: Show this help message.


## Setup ⚙️

1. Clone this repository.
2. Install the required dependencies using the following command:

   ```
   pip install -r requirements.txt
   ```

3. Set up your Discord bot and obtain the bot token.
4. Create a `.env` file in the project directory and add your Discord bot token:

   ```
   DISCORD_TOKEN=your_bot_token_here
   ```

5. Run the bot using `python bot.py`.
 

## Dependencies 📦

- discord.py: For interacting with the Discord API.
- yt-dlp: For extracting information from YouTube URLs.
- python-decouple: For managing environment variables.

---

## Contributing 🤝

Contributions are welcome! If you find any bugs or have suggestions for improvements, please open an issue or submit a pull request.

---

## Credits ❤️

This bot was created by Chihaya. Based on [discord.py](https://github.com/Rapptz/discord.py) and [yt-dlp](https://github.com/yt-dlp/yt-dlp).

--- 