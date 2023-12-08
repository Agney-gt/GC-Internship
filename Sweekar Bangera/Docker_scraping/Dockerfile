# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /app
WORKDIR /app

# Copy only the requirements.txt initially (this helps with caching)
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run webapp.py when the container launches
CMD ["python", "webapp.py"]
