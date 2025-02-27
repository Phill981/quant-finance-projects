FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update -y
RUN apt-get install -y libx11-dev
RUN apt-get install -y python3-tk

COPY . .

CMD ["python", "test.py"]

