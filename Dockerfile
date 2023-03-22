FROM python:3.9-buster
ENV BOT_NAME=$BOT_NAME

WORKDIR /usr/src/app/"${BOT_NAME:-tg_bot}"

COPY requirements.txt /usr/src/app/"${BOT_NAME:-tg_bot}"
COPY alembic /usr/src/app/"${BOT_NAME:-tg_bot}"
COPY alembic.ini /usr/src/app/"${BOT_NAME:-tg_bot}"
RUN pip install -r /usr/src/app/"${BOT_NAME:-tg_bot}"/requirements.txt
COPY tgbot /usr/src/app/"${BOT_NAME:-tg_bot}"
