# Use base Python image
FROM python:3.12-alpine

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV TZ=America/Argentina/Buenos_Aires
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

CMD ["python","app/main.py"]