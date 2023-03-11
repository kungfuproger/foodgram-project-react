FROM python:3.7-slim
WORKDIR /app
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt --no-cache-dir
COPY ./foodgram ./
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --no-input && gunicorn --bind 0:8000 foodgram.wsgi:application"]