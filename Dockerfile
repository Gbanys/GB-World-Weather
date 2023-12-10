FROM python:3.11 as BASE

COPY . /home/GB-World-Weather
WORKDIR /home/GB-World-Weather

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]