FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python manage.py runserver 0.0.0.0:8000

# Expose the necessary ports
EXPOSE 8000