FROM python:3.9-slim
WORKDIR /usr/app
RUN pip install -U pip setuptools wheel
COPY requirements.txt /usr/app/
RUN pip install -r requirements.txt
COPY . /usr/app/
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]