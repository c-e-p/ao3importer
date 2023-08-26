import requests
import time


class Common(object):
	def __init__(self, sess=None):
		if sess is None:
			sess = requests.Session()
		self.sess = sess
		self.req = None
		self.headers = {
			'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit'
			'/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36 +imperfectelena@protonmail.com'
		}

	def recursive_get_data(self, request_url):
		self.req = self.sess.get(request_url, headers=self.headers)
		# if timeout, wait and try again
		while self.req.status_code == 429 or "We've had to block this action to protect our systems" in self.req.text:
			print("timeout... waiting 3 mins and trying again")
			time.sleep(360)
			self.req = self.recursive_get_data(request_url)
		return self.req
