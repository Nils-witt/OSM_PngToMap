FROM python:bookworm

WORKDIR /app
RUN apt-get update && apt-get install libgl1  -y
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./src/ .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["sh","/app/entrypoint.sh"]
