from app.core.celery_app import celery_app


@celery_app.task(bind=True, max_retries=3)
def send_email(self, email: str, subject: str, body: str):
    try:
        print(f"Sending email to {email}")
        return "email_sent"

    except Exception as exc:
        raise self.retry(exc=exc, countdown=5)