import subprocess

# Đường dẫn file cookies
COOKIES_PATH = "cookies.txt"

def get_youtube_audio_url(video_url):
    try:
        # Xây dựng lệnh yt-dlp để lấy URL stream audio
        command = [
            "yt-dlp", "-g", "-f", "bestaudio[ext=m4a]/best",
            "--cookies", COOKIES_PATH, video_url
        ]
        
        # Thực thi lệnh và bắt kết quả trả về
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # Lấy URL audio
        audio_url = result.stdout.strip()
        
        if audio_url:
            return audio_url
        else:
            print("Không tìm thấy URL audio.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi chạy yt-dlp: {e}")
        return None
    except Exception as e:
        print(f"Lỗi không xác định: {e}")
        return None
