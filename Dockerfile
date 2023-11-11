FROM python:3.11 as BASE

ADD . /home/GB-World-Weather
WORKDIR /home/GB-World-Weather
COPY . .

RUN pip install -r requirements.txt

VOLUME ["/data"]

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]