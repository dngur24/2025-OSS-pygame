FROM ubuntu:latest
WORKDIR /app
COPY . .

RUN apt-get update && apt-get upgrade -y 
RUN apt install -y python3-pip && apt install -y python3-git
RUN apt-get -y install python3-venv

RUN apt-get install -y python3-pygame
# RUN apt-get install -y python3-pygame-ce
RUN apt-get install -y python3-tk
# RUN apt-get install -y python3-pygbag

RUN git clone https://github.com/dngur24/2025-OSS-pygame.git