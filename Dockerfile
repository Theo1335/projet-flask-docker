FROM python:3.12-slim
WORKDIR /app
COPY . /app
EXPOSE 5000
RUN pip install --upgrade pip && pip install -r requirements.txt
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "120", "app:app"]