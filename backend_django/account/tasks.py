from celery import shared_task

@shared_task
def welcome_task(username):
    print(f"Celery task executed for user: {username}")
