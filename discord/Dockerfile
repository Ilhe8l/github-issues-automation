FROM python:3.13-slim
RUN pip install --no-cache-dir poetry
WORKDIR /app
COPY pyproject.toml /app/
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root
COPY . /app/
EXPOSE 8501
#CMD ["streamlit", "run", "streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
CMD ["python", "main.py"]
