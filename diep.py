from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.actions.interaction import KEY
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException, JavascriptException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
import os

class Env(object):

	VISU = True

	def __init__(self):
		self.__initVars()
		self.gamemode = 'sandbox'
		self.lastScore = 0
		self.has_exit = False

	def __initVars(self):
		self.driver = self.initDriver()

	def initDriver(self):
		print('Starting driver...', end='', flush=True)
		fo = Options()
		if not Env.VISU:
			fo.headless = True
		fp = webdriver.FirefoxProfile()
		fp.accept_untrusted_certs = True
		fc = webdriver.DesiredCapabilities.FIREFOX
		fc['MARIONETTE'] = False
		fc['acceptSslCerts'] = True
		fc['acceptInsecureCerts'] = True
		driver = webdriver.Firefox(options=fo, capabilities=fc, firefox_profile = fp, executable_path=os.getcwd()+"/geckodriver")
		driver.install_addon(os.getcwd()+'/diep_injector/diep_injector.xpi', temporary=True)
		driver.set_window_position(0, 0)
		driver.set_window_size(1024, 768)
		print('OK')
		return driver

	def reset(self):
		if (self.driver.current_url == "http://diep.io"):
			ActionChains(self.driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
		else:
			print('Getting diep.io...', end='', flush=True)
			self.driver.get("https://diep.io")
			print('OK')
			print('Setting gamemode..', end='', flush=True)
			wait = WebDriverWait(self.driver, 60)
			wait.until(ec.visibility_of_element_located((By.XPATH, "//input")))
			canvas = self.driver.find_element_by_xpath("//canvas")
			ActionChains(self.driver).move_to_element_with_offset(canvas, 597, 58).click().perform()
			print('OK')
			time.sleep(0.5)
		print('Waiting to play...', end='', flush=True)
		wait.until(ec.visibility_of_element_located((By.XPATH, "//input")))
		time.sleep(0.5)
		for _ in range(60):
			try:
				assert self.driver.find_element_by_xpath("//input").is_displayed() == True
			except:
				break
			ActionChains(self.driver).key_down(Keys.ENTER).key_up(Keys.ENTER).perform()
			time.sleep(0.5)
		print('OK')
		return canvas.size

	def close(self):
		print('Exiting')
		self.has_exit = True
		self.driver.close()

	def computeReward(self, observation):
		if 'score' in observation:
			reward = observation['score'] - self.lastScore
			self.lastScore = observation['score']
		return reward

	def step(self, action = {'keys': 0, 'is_clicking': 0, 'mouse_pos': [0,0], 'upgrade': []}):
		self.stepMove(action['keys'])
		self.stepUpgrade(action['upgrade'])
		self.stepMouse(action['is_clicking'], action['mouse_pos'])
		try:
			observation = self.driver.execute_script("return saved_entities")
		except JavascriptException:
			print('JS hasn\'t loaded yet')
			self.close()
			return None, None
		observation.update(self.driver.execute_script("return data"))
		reward = self.computeReward(observation)
		print(reward)
		return observation, reward

	def stepMove(self, val):
		action = ActionChains(self.driver)
		d = [(Keys.UP, 0b0001), (Keys.DOWN, 0b0010), (Keys.LEFT, 0b0100), (Keys.RIGHT, 0b1000)]
		for (k, v) in d:
			if (v & val):
				action.key_down(k)
			else:
				action.key_up(k)
		action.perform()

	def stepUpgrade(self, val):
		action = ActionChains(self.driver)
		for v in val:
			action.send_keys(str(chr(v + 48)))
		action.perform()

	def stepMouse(self, is_click, mouse_pos):
		action = ActionChains(self.driver)
		canvas = self.driver.find_element_by_xpath("//canvas")
		action.move_to_element_with_offset(canvas, mouse_pos[0], mouse_pos[1])
		action.click_and_hold() if is_click else action.release()
		action.perform()
