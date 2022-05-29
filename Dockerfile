FROM python:3.8

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && poetry install --no-dev && python -m spacy download en_core_web_sm

COPY src ./src

COPY model ./model

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0"]