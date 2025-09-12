FROM ubuntu:latest
WORKDIR /app
RUN apt-get update && apt-get upgrade -y 
RUN apt install -y python3-pip && apt install -y python3-git
RUN apt-get install python3-venv

RUN git clone https://github.com/dngur24/2025-OSS-pygame.git

