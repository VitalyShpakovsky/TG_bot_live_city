FROM python:3.11

ENV PYTHONUNBUFFERD=1

WORKDIR /app_tg

RUN pip install --upqrade pip "poetry==1.6.1"
RUN poetry config virtualenvs.create false --local
COPY pyproject.toml ./
COPY poetry.lock ./
RUN poetry install

COPY TG_bot_live_city .

CMD ['python3', 'main.py']