import discord
from discord.ext import commands
import youtube_dl
from requests import get
from youtube_dl import YoutubeDL

YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}

def search(arg):
    with YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            get(arg) 
        except:
            video = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        else:
            video = ydl.extract_info(arg, download=False)

    return video
class music(commands.Cog):
  def __init__(self,client):
    self.client = client
  @commands.command()
  async def join(self, ctx):
    if ctx.author.voice is None:
      await ctx.send("You're not in a voice channel")
    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
      await voice_channel.connect()
    else:
      await ctx.voice_client.move_to(voice_channel)
  @commands.command()
  async def disconnect(self, ctx):
    await ctx.voice_client.disconnect()
  @commands.command()
  async def play(self, ctx, url):
    # ctx.voice_client.stop()
    FFMPEG_OPTIONS = {'before_options' : '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options' : '-vn'}
    YDL_OPTIONS = {'format' : "bestaudio"}
    vc = ctx.voice_client
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
      try:
        info = ydl.extract_info(url, download = False)
        
      except:
        info = search(url)
      url2 = info['formats'][0]['url']
      source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
      vc.play(source)
  @commands.command()
  async def pause(self, ctx):
    await ctx.voice_client.pause()
    await ctx.send("Music Paused!!")
  
  @commands.command()
  async def resume(self, ctx):
    await ctx.voice_client.resume()
    await ctx.send("Music Resumed!!")

def setup(client):
  client.add_cog(music(client))