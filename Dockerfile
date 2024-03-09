FROM python:3.11

ENV PATH="/root/.local/bin:$PATH"

COPY ./poetry.lock ./pyproject.toml main.py ./

RUN apt update -y && \
    apt install pipx -y && \
    apt-get update -y && \
    apt-get install -y swig mupdf mupdf-tools build-essential python3-dev libssl-dev zlib1g-dev libreadline-dev libbz2-dev libsqlite3-dev wget curl llvm libncurses5-dev && \
    pipx ensurepath && \
    pipx install poetry==1.8.2

RUN poetry install --without dev


CMD poetry run python main.py
