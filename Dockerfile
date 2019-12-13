FROM python

COPY . /trading_bot
WORKDIR /trading_bot

RUN /bin/bash -c "source setup_script.sh"

ENV PYTHONPATH=/trading_bot;/trading_bot/venv/lib/python3.6/site-packages
EXPOSE 8000

RUN export

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]