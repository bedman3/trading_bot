FROM python

COPY . /trading_bot
WORKDIR /trading_bot

RUN /bin/bash -c "source setup_script.sh"

RUN which python
ENV PYTHONPATH=/trading_bot;/trading_bot/venv/lib/python3.6/site-packages;/trading_bot/venv/bin

RUN which python
EXPOSE 8000

RUN export

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]