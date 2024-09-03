
# FROM python:3.9-slim

# WORKDIR /app

# COPY . /app

# RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE 5000

# ENV FLASK_APP=app.py

# CMD ["flask", "run", "--host=0.0.0.0"]

FROM python:3.10.12-slim

WORKDIR /app

COPY . /app

# Upgrade pip and set a longer timeout for pip operations
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt --timeout 120

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]
