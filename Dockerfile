# Dùng image chính thức của Python 3.12 làm base
FROM python:3.12-slim

# Thiết lập thư mục làm việc là /app
WORKDIR /app

# Copy các file của project vào /app
COPY . .

# Cập nhật và cài FFmpeg cùng các dependency cần thiết
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Cài đặt các dependency Python
RUN pip install --no-cache-dir -r requirements.txt

# Khai báo cổng mặc định (Render/Railway sẽ tự gán cổng thật qua biến PORT)
EXPOSE 8000

# Lệnh chạy bot - dùng dạng shell (không phải mảng JSON) để đọc được
# biến môi trường $PORT do Render/Railway tự gán. Nếu $PORT không tồn tại
# (ví dụ chạy local) thì mặc định dùng 8000.
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}
