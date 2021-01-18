FROM python:3

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "manage.py", "-c", "api.config", "runserver", "-h", "0.0.0.0", "-p", "5000"]
