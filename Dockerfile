FROM python:3.12

ARG GO_VERSION=1.23.1
RUN apt update && apt install -y build-essential && \
    wget https://golang.org/dl/go$GO_VERSION.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go$GO_VERSION.linux-amd64.tar.gz 
ENV PATH="${PATH}:/usr/local/go/bin"
ENV GOPATH="$HOME/go"
ENV PATH="$PATH:$GOPATH/bin"

VOLUME /logs

WORKDIR /workspace/app/Carcassonne-Neural-Network
COPY ./requirements.txt .
RUN pip install -r requirements.txt

ARG ENGINE_BRANCH=main
WORKDIR /workspace/app
RUN git clone -b $ENGINE_BRANCH --single-branch https://github.com/YetAnotherSpieskowcy/Carcassonne-Engine.git

WORKDIR /workspace/app/Carcassonne-Neural-Network
COPY . .
RUN ENGINE_PATH="../Carcassonne-Engine" make test