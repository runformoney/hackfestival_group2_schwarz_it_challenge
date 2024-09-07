# Use the official Python image
FROM python:3

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY ./ /app

# Install any necessary dependencies
RUN apt-get update && \
apt-get --yes install build-essential ninja-build
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=app.py

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
