# diep-rl

die-rl is a python reinforcement learning environment for [diep.io](https://diep.io/).

**This is not a simulation**, so please use it gently!

---
## Usage
It is made like a [Gym](https://gym.openai.com/) env, so usage is very easy:
```python
import diep
env = diep.Env()
env.reset()
for _ in range(1000):
  action = {'keys': 0, 'is_clicking': 0, 'mouse_pos': [0,0], 'upgrade': []}
  observation, reward = env.step(action)

  if observation['done']:
    observation = env.reset()
env.close()
```
You can launch `demo.py` for a random-action demo of the env

---
## Installation

```bash
./install.sh
```

The install script will install python packages and download geckodriver

---
## Have fun!