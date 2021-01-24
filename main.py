from StocksEnv import StocksEnv, Actions
import StocksData
import CloudStorageClient
import time
import ray
from ray.rllib.agents.ppo import PPOTrainer
from ray.tune import register_env
import pandas
import argparse

# number of previous data points in time to observe
DEFAULT_BARS_COUNT = 10

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--training_data', type=str, help='input training dataset in csv format')
    parser.add_argument('--training_timesteps', type=int, default=50000, help='total timesteps to train for')
    parser.add_argument('--testing_data', type=str, help='input testing dataset in csv format')
    parser.add_argument('--model_file', default='./models/model.zip', type=str, help='output for trained model and/or input for testing model')
    parser.add_argument('--ckpt_path', default=None, type=str, help='checkpoint path')
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

    ray.init()
    config = {
        "lr": 0.01,
        # Use GPUs iff `RLLIB_NUM_GPUS` env var set to > 0.
        "num_gpus": 0,
        "num_workers": 0,
        "framework": "tf",
        "env": "stocks_env"
    }

    if args.training_data:
        stocks_data =  StocksData.read_csv(training_data)
        register_env("stocks_env", lambda config: StocksEnv(stocks_data, bars_count=DEFAULT_BARS_COUNT, reset_on_close=False, commission_perc=0.01))
        stop = {
            # "episode_reward_mean": args.stop_reward,
            "timesteps_total": args.training_timesteps,
        }
        ray.tune.run("PPO", stop=stop, config=config, verbose=1, checkpoint_freq=25000, checkpoint_at_end=True)
    
    if args.testing_data:
        stocks_data =  StocksData.read_csv(testing_data)
        register_env("stocks_env", lambda config: StocksEnv(stocks_data, bars_count=DEFAULT_BARS_COUNT, reset_on_close=False, commission_perc=0.01))
        agent = PPOTrainer(config, env="stocks_env")
        agent.restore(args.ckpt_path)

        stocks_test_env = StocksEnv(stocks_data, bars_count=DEFAULT_BARS_COUNT, reset_on_close=False, commission_perc=0.01)
        obs = stocks_test_env.reset()
        
        # set vars for recording results
        result_df = pandas.DataFrame([], columns=['date', 'open', 'action', 'reward'])
        net_reward = 0.0

        while True:
            action = agent.compute_action(obs)
            obs, reward, done, info = stocks_test_env.step(action)

            # print and record the offset, action taken, reward, opening price
            df = pandas.DataFrame([[stocks_data.date[int(info["offset"])], stocks_data.open[int(info["offset"])], Actions(action).name, reward]], columns=['date', 'open', 'action', 'reward'])
            print(df)
            result_df = result_df.append(df, ignore_index=True)
            net_reward += reward

            # at end of episode, record results and exit
            if done:
                print('Net Reward: ', net_reward)
                result_df.to_csv(result, index=False)
                break

    # upload results if GCS path was given
    if args.result.startswith("gs://"):
        CloudStorageClient.upload_blob(source_file_name=result, destination_blob_name=args.result)

    # upload model if GCS path was given
    if args.model_file.startswith("gs://"):
        CloudStorageClient.upload_blob(source_file_name=model_file, destination_blob_name=args.model_file)
