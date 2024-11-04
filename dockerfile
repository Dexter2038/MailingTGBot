# Use the official Python 3.12.6 image as a base
FROM python:3.12.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Set environment variables
ENV DB_HOST=localhost
ENV DB_USER=myuser
ENV DB_PASSWORD=mypassword
ENV DB_NAME=mydatabase
ENV BOT_TOKEN=your_bot_token
ENV MAIL_USERNAME=your_mail_username
ENV ADMIN=
# default value, will be overridden by Docker run command

# Expose the port (if needed)
# EXPOSE 80  # uncomment if your app needs to expose a port

# Run the command to start the application
CMD ["python", "-m", "app"]
