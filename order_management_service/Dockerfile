FROM python:3.12-slim
WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./app

ENV PYTHONPATH /usr/src/app/app
ENV FLASK_APP app/__init__.py
ENV FLASK_ENV development

RUN adduser --disabled-password --gecos '' myuser
USER myuser

EXPOSE 5000
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5001/ || exit 1

CMD ["flask", "run", "--host=0.0.0.0"]
