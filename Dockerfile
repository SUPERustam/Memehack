# syntax=docker/dockerfile:1
FROM ubuntu:23.10

COPY --link . /memehack
RUN apt-get update && apt install -y python3 \
    python3-pip 
&& rm -rf /var/lib/apt/lists/*

