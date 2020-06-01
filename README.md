# Stock Trading Agent

## Directory Structure
```
stock-trading-agent
│   main.py                 # main script for training and testing
│   StocksEnv.py            # Gym environment for stock trading
│   StocksData.py           # util for processing stock data
│   requirements.txt        # list of Python dependencies
│   Dockerfile              # Docker image reference
│   README.md               # this file
│   
└───datasets                # input stock data for training and testing
│   │   appl_test.csv
│   │   appl_train.csv
│   │   googl_test.csv
│   │   googl_train.csv
│   │   ...
│   
└───models                  # output model files from training
│   │   appl_model.zip
│   │   googl_model.zip
│   │   ...
│
└───results                 # output results from testing
│   │   appl_x_y.csv        # x: net reward, y: timestamp
│   │   googl_x_y.csv
│   │   ...
│
└───tensorboard             # output tensorboard logs while training
    │   TRPO_1
    │   TRPO_2
    │   ...
```

## Quickstart

Note: the following instructions have been tested to work on macOS 10.15.4 with Docker Desktop installed and running

### Obtain Docker Image

To build the image, run the following command from the root directory...
```bash
docker build -t stock-trading-agent:latest .
```

Alternatively, a pre-built image can be downloaded with...
```bash
docker pull raz4/stock-trading-agent:latest
```

### Run Training and Testing

Note: In order to use input files on and output files to the "host" filesystem, the respective volumes must be mounted to the running container. The "-v" options in the following command define the mapping between the host and container directories.

```bash
docker run \
-v "$(pwd)"/models:/app/models \
-v "$(pwd)"/datasets:/app/datasets \
-v "$(pwd)"/results:/app/results \
-v "$(pwd)"/tensorboard:/app/tensorboard \
stock-trading-agent:latest \
--training_data=/app/datasets/appl_train.csv --training_timesteps=20000 --model_file=./models/appl_model --testing_data=/app/datasets/appl_test.csv
```
