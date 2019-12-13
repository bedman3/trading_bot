FROM python

COPY . /trading_bot
WORKDIR /trading_bot

RUN . setup_script.sh

ENV PYTHONPATH=/trading_bot
EXPOSE 8000

RUN export

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]