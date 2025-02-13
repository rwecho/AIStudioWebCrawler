FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update
RUN apt-get install -y libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
libcups2 libdrm2 libdbus-1-3 libxkbcommon0 libatspi2.0-0 libxcomposite1 libxdamage1 \
libxfixes3 libxrandr2 libgbm1 libasound2 libpango-1.0-0 libcairo2
RUN rm -rf /var/lib/apt/lists/*

# 安装 playwright
RUN python -m playwright install --with-deps

COPY . .

RUN mkdir -p /app/logs /app/screenshots

# 复制字体，避免乱码
WORKDIR /usr/share/fonts/chinese/
RUN cp /app/weiruanyahei.ttf /usr/share/fonts/chinese/

WORKDIR /app

CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8000"]
