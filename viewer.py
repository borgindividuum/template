import logging
import ssl
from urllib.request import urlopen, Request
from urllib.error import URLError
from queue import Queue
from threading import Thread
from models import NodeServer
from controllers import make_request


"""

133
134 Host expmain01
135         HostName 54.37.188.114
136         User personaminer
137         IdentityFile /home/cezarsn/.ssh/id_rsa
138
139 Host web01
140         HostName 54.37.188.115
141         User personaminer
142         IdentityFile /home/cezarsn/.ssh/id_rsa
143
144 Host stefnode1
145         HostName 176.223.129.42
146         User personaminer
147         IdentityFile /home/cezarsn/.ssh/id_rsa
148
149 Host cezarnode1
150         HostName 107.191.47.243
151         User personaminer
152         IdentityFile /home/cezarsn/.ssh/id_rsa

"""


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
download_dir = "C:\\temp"


nodes = [NodeServer("https", "explorer.persona.im", "4443", "explorer"),
		NodeServer("http", "45.77.180.23", "4102", "seed mainnet vultr"),
		NodeServer("http", "176.223.129.42", "4102", "seed mainnet vultr"),
		NodeServer("http", "5.135.75.77", "4102", "seed mainnet ovh europe"),
		NodeServer("http", "212.24.100.149", "4102", "server cezar"),
		NodeServer("http", "89.40.7.63", "4102", "interface coors 1, seed server Time4VPS"),
		NodeServer("http", "54.37.188.113", "4102", "interface coors 2"),
		NodeServer("http", "54.37.188.112", "4102", "seed mainnet ovh"),
		NodeServer("http", "54.37.188.114", "4102", "explorer mainnet"),
		NodeServer("http", "192.99.54.32", "4102", "seed mainnet ovh canada"),
		]


class DownloadWorker(Thread):

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            directory, link = self.queue.get()
            try:
            	make_request(link)
                # download_link(directory, link)
            finally:
                self.queue.task_done()

# def download_link(self, link):

# 	req = Request(link, method="GET")
# 	try:
# 		logging.info('Downloading the data from {}'.format(link))
# 		with urlopen(req, 
# 			timeout=1,
# 			context=ssl._create_unverified_context()) as resp:
# 			data = resp.read().decode("utf-8")
			
# 	except URLError as e:
# 		logging.error('Error {} for:  {}'.format(e, link,))
# 	finally:
# 		if "data" in locals():
# 			logging.info('Results for: {} - {}'.format(link, data))


def main():
	queue = Queue()
	for x in range(8):
		worker = DownloadWorker(queue)
		# Setting daemon to True will let the main thread exit even though the workers are blocking
		worker.daemon = True
		worker.start()
	# Put the tasks into the queue as a tuple
	for node in nodes:
		link = node.get_status_url()
		logger.info('Queueing {}'.format(link))
		queue.put((download_dir, link))
    # Causes the main thread to wait for the queue to finish processing all the task
	queue.join()
	logging.info("Done")


if __name__ == "__main__":
	main()
