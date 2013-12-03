import unittest
from DDEXUI.ddex.release import ReleaseIdType, ReleaseType, Release
from DDEXUI.ddex.release_builder import ReleaseBuilder

class ReleaseBuilderTests(unittest.TestCase):
	
	def test_can_build_valid_release(self):
		release = (ReleaseBuilder().title("Black Sands")
			.c_line("copyright ninja tune")
			.p_line("published by ninja")
			.year(2010)
			.reference("R0")
			.release_id(ReleaseIdType.Upc, "5021392584126")
			.release_type(ReleaseType.Single)
			.artist("Bonobo")
			.label("Ninja Tune")
			.parental_warning(True)
			.build())

		self.assertIsInstance(release, Release)

	def test_errors_if_a_non_string_resource_reference_is_passed_in(self):
		self.assertRaises(TypeError, lambda: ReleaseBuilder().reference(123))

		
