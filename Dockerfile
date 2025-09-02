FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY peano_app/ /app/peano_app/

EXPOSE 8080
ENV FLASK_APP=peano_app.app:app
ENV FLASK_ENV=production

CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
