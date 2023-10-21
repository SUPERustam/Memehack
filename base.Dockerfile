FROM ubuntu:20.04

ENV TZ=Europe/Moscow \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3.8 \
    python3-pip \
    libgl1-mesa-glx \
    libglib2.0-0

# COPY layoutparser-0.0.0-py3-none-any.whl /app/

WORKDIR /app

# COPY requirements.txt .

# RUN pip install -r requirements.txt


RUN python3.8 -m pip install https://paddle-qa.bj.bcebos.com/CompileService/train/aarch64/paddlepaddle-2.3.2-cp38-cp38-linux_aarch64.whl # not support 3.9<=
# RUN python3.8 -m pip install layoutparser-0.0.0-py3-none-any.whl

RUN pip install "paddleocr>=2.0.1" --upgrade PyMuPDF==1.21.1

# COPY . .

# EXPOSE 8000

# CMD [ "python3.8", "flask_app.py" ]
ENTRYPOINT ["/bin/bash"]

