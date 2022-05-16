FROM python:3.9.12-slim
ENV PYTHONUNBUFFERED=0
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install mime-support -y
COPY . /app
CMD [ "python3", "-u" ,"main.py" ]