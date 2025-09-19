FROM python:latest

# Initializing work dir
WORKDIR /app

# Installing requierments
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt 

# Copying project
COPY . .

# Run application
CMD [ "python", "app.py" ]
