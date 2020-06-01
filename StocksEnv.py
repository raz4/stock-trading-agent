import enum
import gym
import numpy as np

# cost of buying or selling
DEFAULT_COMMISSION_PERC = 0.05

class Actions(enum.Enum):
    Skip = 0
    Buy = 1
    Close = 2

class StocksEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render.modes': ['human']}

    def __init__(self, prices, bars_count, commission_perc=DEFAULT_COMMISSION_PERC, reset_on_close=True):
        # Actions: Skip, Buy, Close
        self.action_space = gym.spaces.Discrete(n=len(Actions))
        # Observation: volume, high, close, low, open of past x "bars", have position or not, potential profit if sold
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(4*bars_count+1+1,), dtype=np.float32)
        self.bars_count = bars_count
        self._prices = prices
        self.commission_perc = commission_perc
        self.reset_on_close = reset_on_close

    def reset(self):
        self.have_position = False
        self.open_price = 0.0
        self._offset = self.bars_count
        return self.encode()

    def step(self, action):
        reward = 0.0
        done = False
        close = self._cur_close()
        # buy stock if haven't already
        if action == 1 and not self.have_position:
            self.have_position = True
            self.open_price = close
            reward -= self.commission_perc
        # sell stock if bought previously
        elif action == 2 and self.have_position:
            reward -= self.commission_perc
            done |= self.reset_on_close
            reward += 100.0 * (close - self.open_price) / self.open_price
            self.have_position = False
            self.open_price = 0.0

        self._offset += 1
        done |= self._offset >= self._prices.close.shape[0]-1

        # obs, reward, done, info
        return self.encode(), reward, done, {"offset": self._offset, "have_position": self.have_position, "reward": reward, "action": Actions(action).name}
        
    def _cur_close(self):
        """
        Calculate real close price for the current bar
        """
        open = self._prices.open[self._offset]
        rel_close = self._prices.close[self._offset]
        return open * (1.0 + rel_close)

    def encode(self):
        """
        Convert current state into numpy array.
        """
        res = np.ndarray(shape=self.shape, dtype=np.float32)
        shift = 0
        for bar_idx in range(-self.bars_count+1, 1):
            res[shift] = self._prices.high[self._offset + bar_idx]
            shift += 1
            res[shift] = self._prices.low[self._offset + bar_idx]
            shift += 1
            res[shift] = self._prices.close[self._offset + bar_idx]
            shift += 1
            res[shift] = self._prices.volume[self._offset + bar_idx]
            shift += 1
        res[shift] = float(self.have_position)
        shift += 1
        if not self.have_position:
            res[shift] = 0.0
        else:
            res[shift] = (self._cur_close() - self.open_price) / self.open_price
        return res
    
    @property
    def shape(self):
        return (4 * self.bars_count + 1 + 1, )

    def render(self, mode='human', close=False):
        pass

    def close(self):
        pass
    