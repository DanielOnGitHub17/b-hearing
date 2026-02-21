from django.test import TestCase

# Create your tests here.

from .populate_verses import init_bible_db


class TestInitDB(TestCase):
    def test_init_db(self):
        pass
        # self.assertIsNone(
        #     init_bible_db(
        #         "kjv", r"C:\Users\enesi\Code\b-hearing\bible-data\kjv_curated.json"
        #     )
        # )
