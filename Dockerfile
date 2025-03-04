FROM python:3.10

WORKDIR /app

# Copy only requirements.txt first to leverage Docker caching
COPY Backend/requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application files into /app/
COPY Backend/ /app/

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
