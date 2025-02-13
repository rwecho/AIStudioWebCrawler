FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/logs /app/screenshots

# 复制字体，避免乱码
WORKDIR /usr/share/fonts/chinese/
RUN cp /app/weiruanyahei.ttf /usr/share/fonts/chinese/

CMD ["uvicorn", "main_api:app", "--host", "0.0.0.0", "--port", "8000"]
