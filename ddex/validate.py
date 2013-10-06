
class Validate:
	
	def upc(self, text):
		if(len(text) < 12 or len(text) > 13):
			return "upc must be 12 - 13 digit long"
		for char in text:
			try:
				int(char)
				break
			except ValueError:
				return "upc must only contain numbers"
