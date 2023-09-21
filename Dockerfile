FROM python
WORKDIR /api_hh
COPY . /api_hh
#COPY ../requirements.txt /my_api
RUN python -m pip install -r requirements.txt

#COPY /api_hh/my_api /app
#COPY .env /app
#COPY config.py /app
#COPY run.py /app

EXPOSE 5000

LABEL name="My API"

CMD ["python", "run.py"]