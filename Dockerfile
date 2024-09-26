FROM python:3.12 as build

ARG GO_VERSION=1.23.1
RUN apt update && apt install -y build-essential && \
    wget https://golang.org/dl/go$GO_VERSION.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go$GO_VERSION.linux-amd64.tar.gz 
ENV PATH="${PATH}:/usr/local/go/bin"
ENV GOPATH="$HOME/go"
ENV PATH="$PATH:$GOPATH/bin"

VOLUME /logs

WORKDIR /workspace/app/Carcassonne-Neural-Network/
COPY ./requirements.txt ./Makefile ./
RUN python3.12 -m venv .venv && \
    .venv/bin/python -m pip install -r requirements.txt

WORKDIR /workspace/app/
ARG ENGINE_BRANCH=main
RUN git clone -b $ENGINE_BRANCH --single-branch https://github.com/YetAnotherSpieskowcy/Carcassonne-Engine.git

WORKDIR /workspace/app/Carcassonne-Neural-Network/
COPY . .
RUN ENGINE_PATH="../Carcassonne-Engine" make test