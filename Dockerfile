FROM python

COPY . /trading_bot
WORKDIR /trading_bot

ENV PYTHONPATH=/trading_bot;/trading_bot/venv/lib/python3.6/site-packages
RUN /bin/bash -c "source setup_script.sh"

RUN /bin/bash -c "source venv/bin/activate"
ENV PATH=/trading_bot/venv/bin;$PATH

RUN which python
EXPOSE 8000

RUN export

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]