FROM python:3.8.13-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV AM_I_IN_A_DOCKER_CONTAINER True

WORKDIR /app

COPY ./requirements.txt .

RUN pip install  --default-timeout=1000 --upgrade pip \
    && pip install --default-timeout=1000 --no-cache-dir -r requirements.txt

RUN apt update && apt install -y netcat && which nc
COPY ./src /app

ENTRYPOINT ["sh","/app/entrypoint.sh"]

CMD ["python", "/app/utils/pywsgi.py"]

