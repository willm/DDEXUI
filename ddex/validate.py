
class Validate:
	
	def upc(self, text):
		if(len(text) < 12 or len(text) > 13):
			return "upc must be 12 - 13 digits long"
		for char in text:
			if(not self.__number(char)):
				return "upc must only contain numbers"
	
	def year(self, text):
		if(not self.__number(text)):
			return "year must be a number"

	def __number(self, text):
		try:
			int(text)
			return True
		except ValueError:
			return False
	
