from app.core.celery_app import celery_app


@celery_app.task(bind=True, max_retries=5)
def process_refund(self, payment_id: str):
    try:
        print(f"Processing refund for payment {payment_id}")

        # Simulate refund API call
        # call_payment_provider_refund(payment_id)

        return "refund_success"

    except Exception as exc:
        raise self.retry(exc=exc, countdown=10)