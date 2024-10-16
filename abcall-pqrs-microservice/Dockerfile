FROM python:3.12.7

WORKDIR /app

COPY requirements.txt .

RUN pip install chalice

RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD ["chalice", "local", "--host=0.0.0.0", "--no-autoreload"]
