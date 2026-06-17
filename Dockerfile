FROM python:3.11-slim

COPY app.py .

CMD ["python","app.py"]