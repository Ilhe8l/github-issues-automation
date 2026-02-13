FROM python:3.13-slim
RUN pip install --no-cache-dir poetry
WORKDIR /app
COPY pyproject.toml /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root
COPY . /app/
EXPOSE 8501
CMD ["python", "main.py"]
