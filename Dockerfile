FROM python:3.6

RUN mkdir -p /usr/src/FavBet_flask/
WORKDIR /usr/src/FavBet_flask/

COPY . /usr/src/FavBet_flask/
RUN pip install -r requirements.txt

EXPOSE 8080
EXPOSE 5000
EXPOSE 4444

CMD ["flask","run","--host=0.0.0.0", "--port=5000"]