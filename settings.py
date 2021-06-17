from json import load, dump

class Settings:

	def __init__(self):

		#APP CONF
		self.title = "Contact"


		#WINDOW CONF
		base = 75
		ratio = (16, 9)
		self.width = base*ratio[0]
		self.height = base*ratio[1]
		self.screen = f"{self.width}x{self.height}+1000+400"


		#IMG CONF
		self.logo = "img/logo.jpg"

		#DUMMY DATA CONTACTS

		#self.contacts = None
		self.load_data_from_json()


	def load_data_from_json(self):
		with open("data/barang.json", "r") as file_json:
			self.barang = load(file_json)

	def save_data_to_json(self):
		with open("data/barang.json", "w") as file_json:
			dump(self.barang, file_json)