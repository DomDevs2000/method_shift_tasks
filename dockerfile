FROM python:3.13

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN python -m pip install --upgrade pip

COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . /app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
