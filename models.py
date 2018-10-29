from controllers import make_request

class NodeServer():
	def __init__(self, protocol, host, port, description):
		self._status_url = "api/loader/status/sync"
		self._protocol = protocol
		self._host = host
		self._port = port
		self._description = description

	def get_blockheight(self, link):
		controllers.make_request(link)

	def get_status_url(self):
		return "{}://{}:{}/{}".format(self._protocol, self._host, self._port, self._status_url)


	def __str__(self):
		return "{}://{}:{}".format(self._protocol, self._host, self._port)