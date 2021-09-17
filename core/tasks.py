from celery import app
from rest_framework import status
from rest_framework.response import Response
from core.models import Message, Ticket


@app.shared_task
def hello():
    print('hello world')

