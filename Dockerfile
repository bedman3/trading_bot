FROM python

COPY . /trading_bot
WORKDIR /trading_bot

ENV PYTHONPATH=/trading_bot
RUN pip install -r requirements.txt
RUN . download_chromedriver.sh

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]