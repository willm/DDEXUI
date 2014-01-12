from DDEXUI.ddex.release_builder import *
from DDEXUI.ddex.release import *

class TestData:
	@staticmethod
	def release_builder():
		return (ReleaseBuilder().title("Black Sands")
			.c_line("copyright ninja tune")
			.p_line("published by ninja")
			.year(2010)
			.reference("R0")
			.release_id(ReleaseIdType.Upc, "5021392584126")
			.release_type(ReleaseType.Single)
			.artist("Bonobo")
			.label("Ninja Tune")
			.parental_warning(True))
		
