import discord
from discord.ext import commands
import youtube_dl
import asyncio
import random
import nest_asyncio

nest_asyncio.apply()

TOKEN = 'MTM5Njk1NDU3MTUzNTk0NTg4MA.GmmbFy.mXHjREydQSjbg0F5XTzGTmEom221GApl5Y2mfE'

playlist = [
    'https://www.youtube.com/watch?v=pmlqEKklWqs',
    'https://www.youtube.com/watch?v=34HYF3aNU70',
    'https://www.youtube.com/watch?v=cyMuEXEN8nE',
    'https://www.youtube.com/watch?v=_Y8JA7KBBYU',
    'https://www.youtube.com/watch?v=_TvnIykadaM'
]

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

ytdl_format_options = {
    'format': 'bestaudio/best',
    'quiet': True,
    'noplaylist': True,
}
ffmpeg_options = {
    'options': '-vn'
}
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

async def play_song(voice_client, url):
    data = ytdl.extract_info(url, download=False)
    song_url = data['url']
    source = await discord.FFmpegOpusAudio.from_probe(song_url, **ffmpeg_options)
    voice_client.play(source)

async def start_radio(vc):
    while True:
        next_song = random.choice(playlist)
        print(f'🎵 Playing: {next_song}')
        await play_song(vc, next_song)
        while vc.is_playing():
            await asyncio.sleep(1)

@bot.command()
async def fm(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            vc = await channel.connect()
            await ctx.send('📻 FM Radio started!')
            await start_radio(vc)
        else:
            await ctx.send('FM Radio is already running!')
    else:
        await ctx.send('❌ Join a voice channel first!')

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send('⛔ FM Radio stopped')
    else:
        await ctx.send('❌ Not in a voice channel')

# รันบอทแบบนี้
bot.run(TOKEN)


