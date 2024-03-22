# Use the official Python image as the base
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy all the files from the specified directory on your local machine into the container
COPY D:/CodeBackground/Streamlit_app/DarkGPT/ .

# Install any dependencies
RUN pip install --no-cache-dir requirements.txt

# Expose the port that Streamlit runs on
EXPOSE 8501

# Define environment variable
ENV NAME DarkGPT

# Set the entry point to run the Streamlit application
CMD ["streamlit", "run", "app.py"]
