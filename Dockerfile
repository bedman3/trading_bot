FROM python

COPY . /trading_bot
WORKDIR /trading_bot

ENV PYTHONPATH=/trading_bot
RUN pip install -r requirements.txt
RUN chmod +x ./download_chromedriver.sh
RUN ./download_chromedriver.sh
RUN mkdir -p main/static
RUN git clone https://github.com/arteria/django-background-tasks.git
RUN pip install django-background-tasks/
RUN rm -rf django-background-tasks
RUN python manage.py collectstatic --no-input

EXPOSE 8000

CMD ["uwsgi", "--ini", "uwsgi.ini"]