# Carcassonne-Neural-Network

Set of machine learning agents made for game Carcassonne.

## Pre-requirements

### Linux

1. Install Go 1.22 either from your distro's package repositories or by following [instructions on Golang's site](https://go.dev/doc/install)

   **Tip:** If you're using Ubuntu 23.10 or lower, Go version in official repositories is going to be too old.
   You can get the latest version by adding [the PPA listed on Go wiki](https://go.dev/wiki/Ubuntu) and installing `golang` package after.
2. Install `gcc` toolchain from your distro's package repositories (for example, `build-essential` package on Ubuntu).
3. Install Python 3.12 (default version on Ubuntu 24.04, find how to install on your distribution otherwise)

## Installing requirements

```bash
pip install -r requirements.txt
```

Clone latest version of Carcassonne-Engine

```bash
git clone https://github.com/YetAnotherSpieskowcy/Carcassonne-Engine.git
```

## Running the test suite

```bash
ENGINE_PATH="<Path to Carcassonne-Engine repository>" make test
```

## Running docker image

### Based on engine main branch

```bash
docker build -t <IMAGE_NAME> .
docker run --rm -it --entrypoint bash <IMAGE_NAME>
```

### Based on specific engine branch

```bash
docker build --build-arg ENGINE_BRANCH=<BRANCH_NAME> -t <IMAGE_NAME> .
docker run --rm -it --entrypoint bash <IMAGE_NAME>
```
