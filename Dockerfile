FROM python:3
ADD bot.py bot.py
ADD bot.ini bot.ini
ADD requirements.txt requirements.txt
ADD bot bot
RUN pip install -r requirements.txt
RUN pip install -U --pre aiogram
CMD python3 bot.py