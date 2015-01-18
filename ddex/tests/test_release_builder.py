import unittest
from ddex.release import ReleaseIdType, Release
from ddex.release_builder import ReleaseBuilder
from ddex.tests.data_helper import TestData

class ReleaseBuilderTests(unittest.TestCase):
    def test_can_build_valid_release(self):
        release = TestData.release_builder().build()

        self.assertIsInstance(release, Release)

    def test_errors_if_a_non_string_resource_reference_is_passed_in(self):
        self.assertRaises(TypeError, lambda: ReleaseBuilder().reference(123))

    def test_can_get_isrc(self):
        isrc = "FR132131234"
        release_builder = ReleaseBuilder().release_id(ReleaseIdType.Isrc, isrc)
        
        self.assertEqual(release_builder.get_isrc(), isrc)

    def test_can_get_title(self):
        title = "Thriller"
        release_builder = ReleaseBuilder().title(title)
        
        self.assertEqual(release_builder.get_title(), title)
        
    def test_releases_should_only_add_resource_references_once(self):
        subject = ReleaseBuilder()
        reference = "R0"
        subject.add_resource(reference)
        subject.add_resource(reference)

        release = subject.build()

        resource_references = list(map(lambda x: x[0], release.release_resource_references))
        self.assertTrue(resource_references.count(reference) == 1, resource_references)
