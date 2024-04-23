# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port number the Streamlit app runs on
EXPOSE 8501

# Run app.py when the container launches
CMD ["streamlit", "run", "app.py", "--server.port", "8501"]
