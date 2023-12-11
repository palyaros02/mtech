FROM python:3.11-slim as python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH=".venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
      curl

WORKDIR /app

COPY ./pyproject.toml ./poetry.lock* /app/

RUN python3 -m venv $VENV_PATH \
    && chmod +x "$VENV_PATH/bin/activate" \
    && "$VENV_PATH/bin/activate"
RUN curl -sSL https://install.python-poetry.org | python3 -
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-dev

COPY . /app

EXPOSE 8501

CMD ["poetry", "run", "streamlit", "run", "streamlit_app/app.py"]
