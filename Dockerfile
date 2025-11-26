FROM python:3.12.12-trixie

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["streamlit", "run",  "app.py"]