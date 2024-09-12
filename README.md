# Carcassonne-Neural-Network

## Installing requirements

```bash
pip install -r requirements.txt
```

```bash
ENGINE_PATH="<Path to Carcassonne-Engine repository>" make run
```

## Running tests

```bash
python -m pytest test/
```

## Running tests with coverage

```bash
coverage run -m pytest test/ -v -s 
coverage report -m
```
