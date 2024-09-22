FROM python:3.12

ARG GO_VERSION=1.23.1
RUN apt update && apt install -y build-essential && \
    wget https://golang.org/dl/go$GO_VERSION.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go$GO_VERSION.linux-amd64.tar.gz 
ENV PATH="${PATH}:/usr/local/go/bin"
ENV GOPATH="$HOME/go"
ENV PATH="$PATH:$GOPATH/bin"

VOLUME /logs

ARG ENGINE_BRANCH=main
WORKDIR /workspace/app
RUN git clone -b $ENGINE_BRANCH --single-branch https://github.com/YetAnotherSpieskowcy/Carcassonne-Engine.git

WORKDIR /workspace/app/Carcassonne-Engine
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:.

WORKDIR /workspace/app/Carcassonne-Neural-Network
COPY . .
RUN pip install -r requirements.txt
RUN ENGINE_PATH="../Carcassonne-Engine" make test