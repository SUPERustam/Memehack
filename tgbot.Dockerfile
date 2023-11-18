FROM superustam/pre_memehack_tgbot

WORKDIR /app/
COPY config.py config.py
ENV PYTHONPATH="/app/"
ENTRYPOINT ["pypy3", "tg_bot/bot.py"]
