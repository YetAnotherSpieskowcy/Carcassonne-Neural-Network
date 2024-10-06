FROM python:3.12.6-slim-bookworm AS build

ARG GO_VERSION=1.23.1
RUN apt-get update && apt-get install -y build-essential wget && \
    wget https://golang.org/dl/go$GO_VERSION.linux-amd64.tar.gz && \
    tar -C /usr/local -xzf go$GO_VERSION.linux-amd64.tar.gz && \
    rm -rf /var/lib/apt/lists/*

ENV PATH="${PATH}:/usr/local/go/bin"
ENV GOPATH="$HOME/go"
ENV PATH="$PATH:/go/bin"


ARG ENGINE_BRANCH=main
ADD https://github.com/YetAnotherSpieskowcy/Carcassonne-Engine.git#$ENGINE_BRANCH /engine
RUN make build-python -C /engine

FROM python:3.12.6-slim-bookworm
RUN apt-get update && apt-get install -y build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

VOLUME /logs

WORKDIR /Carcassonne-Neural-Network/
COPY ./requirements.txt ./Makefile ./
RUN make .venv

COPY --from=build /engine/built_wheels /Carcassonne-Engine/built_wheels

COPY src src
COPY test test
RUN ENGINE_PATH="../Carcassonne-Engine" make test

WORKDIR /workspace
ENTRYPOINT ["/Carcassonne-Neural-Network/.venv/bin/python"]
