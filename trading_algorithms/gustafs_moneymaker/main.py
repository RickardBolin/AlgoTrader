from datetime import datetime


class Bot:

	def __init__(self):
		self.name = "boiiii"

	def algorithm(self, data):
		return {"actions": [(datetime.fromtimestamp(1545730073),"buy",1000), (datetime.fromtimestamp(1545770073),"sell",1000)]}
