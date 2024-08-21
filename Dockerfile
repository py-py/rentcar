FROM python:3.9.19-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app

CMD python manage.py migrate && python3 manage.py collectstatic --noinput && gunicorn rentie.wsgi

