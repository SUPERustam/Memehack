# syntax=docker/dockerfile:1
FROM ubuntu:20.04

# old
# COPY --link . /memehack
# RUN apt-get update && apt install -y python3 \
#     python3-pip 
# && rm -rf /var/lib/apt/lists/*


LABEL maintainer=498rustam@gmail.com
ENV TZ=Asia/Kolkata \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt-get update && apt-get install -y \
    python3-venv \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* /tmp/apt-packages

RUN python3 -m venv .env
COPY . .
# RUN pip install -r requirements.txt
RUN /bin/bash -c ". ./.env/bin/activate" \ 
    && pip install -U https://paddle-qa.bj.bcebos.com/CompileService/train/aarch64/paddlepaddle-2.3.2-cp38-cp38-linux_aarch64.whl \
    paddleocr>=2.0.1 \
    PyMuPDF==1.21.1 \
    && rm -rf /root/.cache /tmp/pip-* /tmp/pip3-packages


# RUN pip install https://paddle-qa.bj.bcebos.com/CompileService/train/aarch64/paddlepaddle-2.3.2-cp38-cp38-linux_aarch64.whl
# RUN /opt/venv/bin/pip install "paddleocr>=2.0.1" --upgrade PyMuPDF==1.21.1

# EXPOSE 8000
# CMD [ "python3", "flask_app.py" ]

