FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /arkon_api
COPY requirements.txt requirements.txt
RUN apt-get update
RUN apt install -y build-essential
RUN pip install --upgrade setuptools
RUN pip install Cython
RUN apt-get install -y default-libmysqlclient-dev
RUN pip install -r requirements.txt
COPY . .
#CMD ["python","manage.py","runserver","0.0.0.0:8000"]