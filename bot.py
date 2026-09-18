import discord
from discord.ext import commands
import asyncio
from MusicaBot.buscar import search_youtube
from MusicaBot.audio import get_youtube_audio_url
from youtube_search import YoutubeSearch
import os
from dotenv import load_dotenv
import json

# Nạp các biến môi trường từ file .env
load_dotenv()

class MusicBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents().all())
        self.voice_client = None
        self.music_queue = []  # Hàng đợi lưu các URL nhạc
        self.is_playing = False  # Cờ đánh dấu trạng thái đang phát
    


    async def play_music(self, user_id, channel_id, guild_id, query):

        try:
            print(f"Đang tìm audio cho truy vấn: {query}")
            guild = self.get_guild(int(guild_id))
            if guild is None:
                print("Không tìm thấy server.")
                return "Bot không có trong server được chỉ định."
            

            member = guild.get_member(int(user_id))
            if member is None:
                print("Người dùng không có trong server.")
                return "Người dùng không có trong server."

            # Kiểm tra xem người dùng có đang trong kênh thoại không
            if member.voice is None or member.voice.channel.id != int(channel_id):
                print("Người dùng không ở đúng kênh thoại.")
                return f"Người dùng {user_id} không ở đúng kênh thoại."

            # Tìm audio YouTube dựa trên truy vấn
            extract = search_youtube(query)

            results = YoutubeSearch(extract, max_results=1).to_json()
            data_url = json.loads(results)
            



            

            url = get_youtube_audio_url(extract)

            if not url:
                raise ValueError("Không lấy được URL audio.")

            # Thêm URL vào hàng đợi nhạc
            self.music_queue.append(url)
            print(f"Đã thêm vào hàng đợi: {url}. Hàng đợi hiện tại: {self.music_queue}")

            # Nếu bot chưa phát nhạc, bắt đầu phát
            if self.voice_client is None:
                # Kết nối tới kênh thoại
                self.voice_client = await member.voice.channel.connect()

            # Bắt đầu phát nếu chưa có nhạc nào đang phát
            if not self.is_playing:
                asyncio.create_task(self.start_playing())  # Phát nhạc ở chế độ nền

            # Gửi phản hồi JSON ngay lập tức
            
            return {"status": "success", "message": "Đã thêm bài hát vào hàng đợi", "queue": self.music_queue, "info_music": data_url}

        except Exception as e:
            print(f"Lỗi khi phát nhạc: {e}")
            return {"status": "error", "message": str(e)}

    async def start_playing(self):
        # Xử lý phát nhạc trong hàng đợi
        while self.music_queue:
            url = self.music_queue.pop(0)  # Lấy URL tiếp theo trong hàng đợi

            # Các tuỳ chọn FFmpeg đã được cải thiện
            ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                              'options': '-vn -loglevel panic'}

            self.is_playing = True
            # Phát audio
            self.voice_client.play(discord.FFmpegPCMAudio(url, **ffmpeg_options), after=self.check_queue)

            # Đợi cho đến khi phát xong
            while self.voice_client.is_playing():
                await asyncio.sleep(1)

        # Ngắt kết nối sau khi hết hàng đợi
        if self.voice_client:
            await self.voice_client.disconnect()
            self.voice_client = None
        self.is_playing = False

    def check_queue(self, error=None):
        if error:
            print(f"Lỗi khi phát: {error}")
        # Gọi start_playing để phát bài tiếp theo trong hàng đợi
        if self.music_queue:
            asyncio.create_task(self.start_playing())

    async def show_queue(self):
        return self.music_queue  # Trả về hàng đợi hiện tại

    async def on_ready(self):
        print(f"Bot đã kết nối với tên {self.user} trên server.")

    async def start_bot(self):
        # Khởi động bot
        TOKEN = os.getenv("DISCORD_TOKEN")
        await self.start(TOKEN)
