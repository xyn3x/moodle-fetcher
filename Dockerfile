FROM python:latest

# Insalling cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Initializing work dir
WORKDIR /app

# Installing requierments
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt 

# Copying project
COPY . .

# Init cron with permissions
RUN echo "0 */12 * * * /usr/local/bin/python /app/app.py >> /proc/1/fd/1 2>> /proc/1/fd/2" > /etc/cron.d/my-cron \
    && chmod 0644 /etc/cron.d/my-cron \
    && crontab /etc/cron.d/my-cron

CMD ["cron", "-f"]


