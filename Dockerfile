# Use an official Python runtime as a parent image
FROM python:2.7-slim
RUN apt-get update

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD ./flask_app.py /app
ADD ./knowledge.py /app
ADD ./knn.algo /app
ADD ./movies.json /app
ADD ./requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN apt-get --assume-yes install gcc
RUN pip install numpy
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable
ENV FLASK_APP flask_app.py

# Run flask_app.py when the container launches
CMD ["flask", "run", "--host=0.0.0.0"]