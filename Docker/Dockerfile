# Use the official Python image as the base image
FROM python:3.13-alpine

# Set the working directory in the container
WORKDIR /app

# Install bash, git, curl, and dcron
RUN apk add --no-cache bash git curl dcron

# Remove any existing files in the /app directory
RUN rm -rf /app/*

# Clone the repository
RUN git clone https://github.com/Obijuan88/ETSweatherproject.git /app

# Set the working directory to the cloned repository
WORKDIR /app/ETSweatherproject

# Copy the requirements file into the container
COPY ../requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for Python path
ENV PYTHONPATH=/app/src

# Copy the local .env file into the container
COPY ../.env /app/.env

RUN chmod +x /app/ETSweatherproject/src/telegramsub.py
# Add the cron job

COPY cronjob /var/spool/cron/crontabs/root
RUN chmod 600 /var/spool/cron/crontabs/root

RUN touch /var/log/cron.log
# Copy the startup script
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Use the startup script as the CMD
CMD ["/start.sh"]
