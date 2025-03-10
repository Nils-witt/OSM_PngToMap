FROM python:slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY ./src/ .


EXPOSE 8080
CMD ["gunicorn", "-b", ":8080", "app"]