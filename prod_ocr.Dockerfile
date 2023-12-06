# syntax=docker/dockerfile:1
FROM ubuntu:20.04

LABEL maintainer=498rustam@gmail.com
ENV TZ=Europe/Moscow \
    DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y \
    curl \
    git \
    software-properties-common \
    libgl1-mesa-glx \ 
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/* /tmp/apt-packages

RUN add-apt-repository ppa:deadsnakes/ppa \
    && add-apt-repository universe \
    && rm -rf /var/lib/apt/lists/* /tmp/apt-packages
  # python3.9-distutils \

RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* /tmp/apt-packages

# RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.8

WORKDIR /app

# RUN /bin/bash -c ". ./.env/bin/activate" && \ 
RUN pip install paddlepaddle -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN python3.8 -m pip install --no-cache-dir "paddleocr>=2.0.1" \
    -U "PyMuPDF==1.21.1" 

COPY --link upload_module/ upload_module/ 
RUN pip install --no-cache-dir -r upload_module/requirements.txt
COPY --link util.py util.py
COPY --link config.py config.py
COPY --link db/ db/

ENV PYTHONPATH=/app
ENTRYPOINT ["python3", "-O", "upload_module/pipeline.py", "76552532", "139105204", "tg_img_upload"]
