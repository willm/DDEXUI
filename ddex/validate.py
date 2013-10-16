
class Validate:
	
	def upc(self, text):
		result = {}
		result["success"] = False
		if(len(text) < 12 or len(text) > 13):
			result["error"] = "upc must be 12 - 13 digits long"
		for char in text:
			if(not self.__number(char)):
				result["error"] = "upc must only contain numbers"
		if(not "error" in result):
			result["value"] = text
			result["success"] = True
		return result
	
	def year(self, text):
		result = {}
		result["success"] = False
		if(not self.__number(text)):
			result["error"] = "year must be a number"
		if(not "error" in result):
			result["value"] = int(text)
			result["success"] = True
		return result
		

	def __number(self, text):
		try:
			int(text)
			return True
		except ValueError:
			return False

	def not_empty(self, text):
		result = {}
		if(text == ""):
			result["error"] = "value cannot be empty"
			result["success"] = False
		else:
			result["success"] = True
			result["value"] = text
		return result
