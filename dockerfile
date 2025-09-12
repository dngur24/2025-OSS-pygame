FROM ubuntu:latest

RUN apt update && apt upgrade 
RUN apt install -y python3-pip && apt install -y python3-git
RUN git clone https://github.com/dngur24/2025-OSS-pygame.git

RUN apt install -y python3-requirements.txt


