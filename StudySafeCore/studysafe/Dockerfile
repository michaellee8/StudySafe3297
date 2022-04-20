FROM python:3.8

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

RUN python3 manage.py collectstatic

CMD python3 manage.py runserver 0.0.0.0:8000