FROM python:3.12-slim
WORKDIR /app
COPY . /app
EXPOSE 5000
RUN pip install -r /app/requirements.txt
CMD ["python", "app.py"]