FROM python:3.7.6-slim
# install system dependencies
RUN apt-get update && apt install -y libopenmpi-dev libglib2.0-0 libsm6 libxrender1

WORKDIR '/app'

# install python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy app specific dirs and files
ADD datasets ./datasets
ADD models ./models
COPY main.py StocksData.py StocksEnv.py ./

ENTRYPOINT [ "python", "main.py" ]
