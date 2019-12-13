FROM python

COPY . /trading_bot
WORKDIR /trading_bot

SHELL ["/bin/bash", "-c", "source setup_script.sh"]
RUN export

ENV PYTHONPATH=/trading_bot
EXPOSE 8000

RUN /bin/bash -c "export"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]