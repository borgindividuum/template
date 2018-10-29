import logging
import ssl
from urllib.request import urlopen, Request
from urllib.error import URLError

def make_request(link):

	req = Request(link, method="GET")
	try:
		logging.info('Connection with: {}'.format(link))
		with urlopen(req, 
			timeout=1,
			context=ssl._create_unverified_context()) as resp:
			data = resp.read().decode("utf-8")
			
	except URLError as e:
		logging.error('Error {} for:  {}'.format(e, link,))
	finally:
		if "data" in locals():
			logging.info('Results for: {} - {}'.format(link, data))
