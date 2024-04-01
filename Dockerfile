FROM python:3.8.5

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

COPY app /usr/src/app

CMD ["python", "app/main.py"]


