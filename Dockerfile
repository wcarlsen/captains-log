FROM python:3.8-alpine

WORKDIR /app

COPY Pipfile* ./

RUN pip install --no-cache-dir pipenv \
    && pipenv install --system --deploy --clear \
    && pip uninstall pipenv -y

COPY src/ .
COPY service.py .

ENTRYPOINT ["python", "service.py"]