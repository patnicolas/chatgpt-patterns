FROM python:3.9
WORKDIR .
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python3", "./src/main.py"]

