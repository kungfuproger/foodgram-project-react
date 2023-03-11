FROM python:3.7-slim
WORKDIR /app
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt --no-cache-dir
COPY ./foodgram ./
COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
CMD ["gunicorn", "--bind", "0:8000", "foodgram.wsgi:application"]
