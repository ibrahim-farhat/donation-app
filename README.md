# donation-app
This repo. includes the donation project, which will be made using django web framework.

# Running Instructions
1- cd blood_bank/
2- python manage.py runserver
3- go to another terminal
4- cd blood_bank/
5- docker pull rabbitmq:3.13.1-management
6- docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13.1-management
7- celery -A blood_bank worker -l info
8- docker pull redis:7.2.4
9- docker run -it --rm --name redis -p 6379:6379 redis:7.2.4
10- go to another terminal
11- cd blood_bank/
12- celery -A blood_bank beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler