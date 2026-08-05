import unittest

from qualysdk.tagging.data_classes.Tag import Tag, TagSimple


class TestTagUuid(unittest.TestCase):
    def test_tag_from_dict_accepts_tagUuid(self):
        tag = Tag.from_dict(
            {
                "id": 123,
                "name": "prod",
                "tagUuid": "7e9a3f2c-1111-2222-3333-444455556666",
            }
        )
        self.assertEqual(tag.tagUuid, "7e9a3f2c-1111-2222-3333-444455556666")

    def test_tag_from_dict_accepts_all_xsd_fields(self):
        tag = Tag.from_dict(
            {
                "id": 123,
                "name": "prod",
                "tagUuid": "7e9a3f2c-1111-2222-3333-444455556666",
                "parentTagUuid": "aaaaaaaa-bbbb-cccc-dddd-eeeeffff0000",
                "srcOperatingSystemName": "Windows",
                "reEvalStatusProgress": 0.5,
                "scopeLimiterId": 42,
                "isSubUserScopedTag": True,
            }
        )
        self.assertEqual(tag.parentTagUuid, "aaaaaaaa-bbbb-cccc-dddd-eeeeffff0000")
        self.assertEqual(tag.srcOperatingSystemName, "Windows")
        self.assertEqual(tag.reEvalStatusProgress, 0.5)
        self.assertEqual(tag.scopeLimiterId, 42)
        self.assertIs(tag.isSubUserScopedTag, True)

    def test_tag_simple_from_dict_accepts_tagUuid(self):
        child = TagSimple.from_dict(
            {"id": 1, "name": "child", "tagUuid": "abc-123", "parentTagUuid": "def-456"}
        )
        self.assertEqual(child.tagUuid, "abc-123")
        self.assertEqual(child.parentTagUuid, "def-456")


if __name__ == "__main__":
    unittest.main()
