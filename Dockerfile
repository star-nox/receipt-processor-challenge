FROM python:3.10.11

WORKDIR /receipt-processor-challenge

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["flask", "--app", "main:app", "--debug", "run", "--port", "8000"]