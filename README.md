# My Python Flask App
flask app
This is simple mail sending flask app I built.

It uses flask, a celery task handler and redis queue.


Setup and Commands used :

1)sudo service rabbitmq-server restart               //rabbit mq in ubuntu bash
2) celery -A web.celery worker --loglevel=info       //in seperate terminal 
3)python web.py                                      // in seperate terminal

Then go to localhost:5000 in  the browser.
