# syntax=docker/dockerfile:1
FROM ubuntu:20.04

LABEL maintainer=498rustam@gmail.com
ENV TZ=Europe/Moscow \
    DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    curl \
    git \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/* /tmp/apt-packages

RUN add-apt-repository ppa:deadsnakes/ppa \
    && add-apt-repository universe \
    && rm -rf /var/lib/apt/lists/* /tmp/apt-packages
  # python3.9-distutils \

RUN apt-get update && eapt-get install -y \
    python3.8 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/* /tmp/apt-packages

# RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.8

WORKDIR /app

# RUN pip install -r requirements.txt
RUN /bin/bash -c ". ./.env/bin/activate" \ 
    && python3 -m pip install -U https://paddle-qa.bj.bcebos.com/CompileService/train/aarch64/paddlepaddle-2.3.2-cp38-cp38-linux_aarch64.whl \
    "paddleocr>=2.0.1" \
    "PyMuPDF==1.21.1" \
    && rm -rf /root/.cache /tmp/pip-* /tmp/pip3-packages

RUN git clone --quiet https://github.com/win0err/aphrodite-terminal-theme ~/.bash/themes/aphrodite \
    && echo 'source ~/.bash/themes/aphrodite/aphrodite.theme.sh\n shopt -s autocd > /dev/null\n alias python=python3.9\n alias pip=pip3' >> ~/.bashrc

ENTRYPOINT ["/bin/bash"]

# EXPOSE 8000
# CMD [ "python3", "flask_app.py" ]
