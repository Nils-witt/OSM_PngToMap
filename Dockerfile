FROM python:bookworm
WORKDIR /app
RUN apt-get update && apt-get install libgl1  -y
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY ./src/ .


EXPOSE 8080
CMD ["gunicorn", "-b", ":8080", "app"]