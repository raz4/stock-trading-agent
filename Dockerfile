FROM python:3.7.6-slim
# install system dependencies
RUN apt-get update && apt install -y libglib2.0-0

WORKDIR '/app'

# install python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy app specific dirs and files
ADD datasets ./datasets
ADD ray_results ./ray_results
ADD results ./results
COPY main.py StocksData.py StocksEnv.py CloudStorageClient.py ./

ENTRYPOINT [ "python", "main.py" ]
