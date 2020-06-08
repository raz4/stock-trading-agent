from StocksEnv import StocksEnv, Actions
import StocksData
import CloudStorageClient
import time
from stable_baselines.common.policies import MlpPolicy
from stable_baselines import TRPO
import pandas
import argparse

# number of previous data points in time to observe
DEFAULT_BARS_COUNT = 10

def train(training_data, training_timesteps, model_file):
    stocks_data =  StocksData.read_csv(training_data)
    stocks_env = StocksEnv(stocks_data, bars_count=DEFAULT_BARS_COUNT, reset_on_close=False, commission_perc=0.01)
    model = TRPO(MlpPolicy, stocks_env, verbose=1, tensorboard_log="./tensorboard/")
    model.learn(total_timesteps=training_timesteps)
    model.save(model_file)

def test(testing_data, model_file, result):
    model = TRPO.load(model_file)

    # set testing environment
    stock_test_data =  StocksData.read_csv(testing_data)
    stocks_test_env = StocksEnv(stock_test_data, bars_count=10, reset_on_close=False)
    obs = stocks_test_env.reset()

    # set vars for recording results
    result_df = pandas.DataFrame([], columns=['date', 'open', 'action', 'reward'])
    net_reward = 0.0

    while True:
        action, _states = model.predict(obs)
        obs, reward, done, info = stocks_test_env.step(action)

        # print and record the offset, action taken, reward, opening price
        df = pandas.DataFrame([[stock_test_data.date[int(info["offset"])], stock_test_data.open[int(info["offset"])], Actions(action).name, reward]], columns=['date', 'open', 'action', 'reward'])
        print(df)
        result_df = result_df.append(df, ignore_index=True)
        net_reward += reward

        # at end of episode, record results and exit
        if done:
            print('Net Reward: ', net_reward)
            result_df.to_csv(result, index=False)
            break

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--training_data', type=str, help='input training dataset in csv format')
    parser.add_argument('--training_timesteps', type=int, default=50000, help='total timesteps to train for')
    parser.add_argument('--testing_data', type=str, help='input testing dataset in csv format')
    parser.add_argument('--model_file', default='./models/model.zip', type=str, help='output for trained model and/or input for testing model')
    parser.add_argument('--result', default='./results/result.csv', type=str, help='output for testing results based on trained model')
    args = parser.parse_args()

    training_data = args.training_data
    if args.training_data and args.training_data.startswith("gs://"):
        training_data = "./datasets/" + training_data.split('/')[-1]
        CloudStorageClient.download_blob(source_blob_name=args.training_data, destination_file_name=training_data)
    
    model_file = "./models/" + args.model_file.split('/')[-1] if args.model_file.startswith("gs://") else args.model_file
    if args.model_file.startswith("gs://") and not args.training_data:
        CloudStorageClient.download_blob(source_blob_name=args.model_file, destination_file_name=model_file)
    
    testing_data = args.testing_data
    if args.testing_data and args.testing_data.startswith("gs://"):
        testing_data = "./datasets/" + testing_data.split('/')[-1]
        CloudStorageClient.download_blob(source_blob_name=args.testing_data, destination_file_name=testing_data)

    result = args.result
    if result.startswith("gs://"):
        result = "./results/" + model_file.split('/')[-1].split(".zip")[0] + "_" + str(time.time()).replace('.', '') + ".csv"

    if args.training_data:
        train(training_data=training_data, training_timesteps=args.training_timesteps, model_file=model_file)
    
    if args.testing_data:
        test(testing_data=testing_data, model_file=model_file, result=result)

    # upload results if GCS path was given
    if args.result.startswith("gs://"):
        CloudStorageClient.upload_blob(source_file_name=result, destination_blob_name=args.result)

    # upload model if GCS path was given
    if args.model_file.startswith("gs://"):
        CloudStorageClient.upload_blob(source_file_name=model_file, destination_blob_name=args.model_file)
