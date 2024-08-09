FROM python:3.8-slim

# Set the working directory
WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*
    
# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Create the uploads, flagged, and matplotlib_cache directories with proper permissions
RUN mkdir -p  /app/flagged /app/matplotlib_cache && chmod -R 777 /app/uploads /app/flagged /app/matplotlib_cache

# Set the MPLCONFIGDIR environment variable
ENV MPLCONFIGDIR=/app/matplotlib_cache

# Run the application
CMD ["python", "app.py"]
