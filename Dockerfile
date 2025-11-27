FROM python:3.12.12-trixie

# Update the package lists
RUN apt-get update

# Install git package
RUN apt-get install -y git

# Install Git and clean up the package cache in one layer
RUN rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["streamlit", "run",  "app.py", "--server.port=8080"]