
class Validate:
	
	def upc(self, text):
		result = {}
		if(len(text) < 12 or len(text) > 13):
			result["error"] = "upc must be 12 - 13 digits long"
		for char in text:
			if(not self.__number(char)):
				result["error"] = "upc must only contain numbers"
		if(not "error" in result):
			result["value"] = text
		return result
	
	def year(self, text):
		result = {}
		if(not self.__number(text)):
			result["error"] = "year must be a number"
		if(not "error" in result):
			result["value"] = int(text)
		return result
		

	def __number(self, text):
		try:
			int(text)
			return True
		except ValueError:
			return False
	
