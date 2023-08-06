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

	# todo this isn't actually recursive yet...
	def recursive_get_data(self, request_url):
		self.req = self.sess.get(request_url)
		# if timeout, wait and try again
		while self.req.status_code == 429:
			print("timeout... waiting 3 mins and trying again")
			time.sleep(360)
			self.req = self.sess.get(request_url, headers=self.headers)
		return self.req
