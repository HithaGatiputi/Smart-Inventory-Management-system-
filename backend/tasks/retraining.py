
from celery import Celery

app = Celery(
    "tasks",
    broker="redis://redis:6379/0"
)

@app.task
def retrain_models():
    print("Retraining started")
