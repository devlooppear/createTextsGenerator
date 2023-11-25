FROM python:3.11.2

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip freeze > requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install nltk

RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run script.py when the container launches
CMD ["python", "script.py"]
