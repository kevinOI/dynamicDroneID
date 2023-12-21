FROM python:3.10-slim-bookworm

COPY . /app
WORKDIR /app

RUN apt update && apt install -y \
	build-essential
RUN pip install pyserial pymavlink

CMD ["python", "dynamicdroneid.py"]
