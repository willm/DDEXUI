import unittest
from datetime import timedelta
from mutagenx.mp3 import MP3

class DurationFormatterTests(unittest.TestCase):

	def setUp(self):
		self.subject = DurationFormatter()
		#self.duration = self.subject.get_duration("./ddex/tests/resources/test.mp3")
		self.duration = self.subject.get_duration("ddex/tests/resources/test.mp3")

	def test_should_have_commercial_model_type(self):
		self.assertEqual(self.duration, "PT0M4.000S")

class DurationFormatter():

	def get_duration(self, file_path):
		total_seconds = MP3(file_path).info.length
		print(total_seconds)
		minutes = int(total_seconds / 60)
		seconds = int(total_seconds % 60)
		return "PT" + str(minutes) + "M" + str(seconds) + ".000S"
