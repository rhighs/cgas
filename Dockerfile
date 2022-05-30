FROM python:3.9.12-slim
ENV PYTHONUNBUFFERED=0
WORKDIR /app
RUN python -m venv /opt/Telegram
# Enable venv
ENV PATH="/opt/Telegram/bin:$PATH"
RUN sh /opt/Telegram/bin/activate
COPY main.py main.py
COPY keys.json keys.json
COPY requirements.txt requirements.txt
#COPY to_install to_install
COPY cloudygram_api_server cloudygram_api_server
#RUN pip3 install -r requirements.txt -f to_install
RUN pip3 install -r requirements.txt
COPY .Telegram/Lib/site-packages/telethon /opt/Telegram/lib/python3.9/site-packages/telethon
CMD [ "python3", "-u" ,"main.py" ]