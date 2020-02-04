FROM python:slim-buster
RUN apt update && apt install -y python3-pip
RUN pip install sendgrid
WORKDIR /app
COPY index.py /app/index.py
CMD ["python","-u","index.py"]
