# Grocery Store

## Description:
Grocery Store is a multi-user app where user can buy various products from different catogories.
In this app ,admin has the ability to approve or reject store manager requests while store
can make changes in products section.This app also implements dynamic pricing i.e price vary
according to demand.


## Instructions to Run the App
* python app.py in WSL
* start redis server on windows
* start worker in ubuntu
"celery -A app.celery worker -l info -E"
* start beat in windows
"celery -A app.celery beat --max-interval 1 -l info"
* mailhog in WSL
 "~/go/bin/MailHog"
* In the project folder terminal
 npm run serve

