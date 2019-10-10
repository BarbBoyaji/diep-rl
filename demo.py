import random
import time
import diep
import signal

def demo1(env):
	action = {'keys': 0, 'is_clicking': 0, 'mouse_pos': [0,0], 'upgrade': []}
	start = time.time()
	while 1:
		if (round(time.time() - start) % 4 == 0):
			action = {'keys': 0b0101, 'is_clicking': 0, 'mouse_pos': [(dims[0]/4)*3,(dims[1]/4)], 'upgrade':[]}
		elif (round(time.time() - start) % 4 == 1):
			action = {'keys': 0b0110, 'is_clicking': 1, 'mouse_pos': [(dims[0]/4),(dims[1]/4)*3], 'upgrade':[1,3,4]}
		elif (round(time.time() - start) % 4 == 2):
			action = {'keys': 0b1010, 'is_clicking': 0, 'mouse_pos': [(dims[0]/4)*3,(dims[1]/4)*3], 'upgrade':[]}
		elif (round(time.time() - start) % 4 == 3):
			action = {'keys': 0b1001, 'is_clicking': 1, 'mouse_pos': [(dims[0]/4),(dims[1]/4)], 'upgrade':[]}
		env.step(action)

def demo2(env):
	action = {'keys': 0, 'is_clicking': 0, 'mouse_pos': [0,0], 'upgrade': []}
	start = time.time()
	# cv2.startWindowThread()
	# cv2.namedWindow("preview")
	while not env.has_exit:
		action = {
		'keys': random.choice([0b0100, 0b1000]) | random.choice([0b0010, 0b0001]),
		'is_clicking': random.choice([0,1,1,1,1]),
		'mouse_pos': [random.randint(0,dims[0]),random.randint(0,dims[1])],
		'upgrade':[random.randint(1,9)]
		}
		obs, reward = env.step(action)
		if (obs.get('done') == True):
			env.reset()
		time.sleep(random.randrange(0,1))

env = diep.Env()
dims = list(env.reset().values())
dims = [dims[1], dims[0]]
action = {'keys': 0, 'is_clicking': 0, 'mouse_pos': [0,0], 'upgrade': []}
demo2(env)
