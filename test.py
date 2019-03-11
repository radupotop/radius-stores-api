import unittest
from run import app


class TailsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.test_client = app.test_client()

    def test_get_all(self):
        response = self.test_client.get('/')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(len(response.json['results']), 95)

    def test_lookup_partial_postcode_1(self):
        """
        Lookup postcode or partial postcode.
        """
        response = self.test_client.get('/?postcode=SW11')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(len(response.json['results']), 1)

    def test_lookup_partial_postcode_2(self):
        """
        Lookup postcode or partial postcode.
        """
        response = self.test_client.get('/?postcode=GU')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(len(response.json['results']), 6)

    def test_lookup_postcode_radius_01(self):
        """
        Lookup nearby stores based on exact match of `postcode` and
        a small `radius` parameter.
        """
        response = self.test_client.get('/?nearby=NW1+9EX&radius=0.1')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(len(response.json['results']), 4)

    def test_lookup_postcode_default_radius_high_density(self):
        """
        Lookup nearby stores based on exact match of `postcode` and
        the default radius param, in a high density area - Camden.
        """
        response = self.test_client.get('/?nearby=NW1+9EX')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(len(response.json['results']), 23)

    def test_lookup_postcode_default_radius_lower_density(self):
        """
        Lookup nearby stores based on exact match of `postcode` and
        the default radius param, in a lower density area.
        """
        response = self.test_client.get('/?nearby=SG13+7RQ')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(len(response.json['results']), 7)


if __name__ == '__main__':
    unittest.main(verbosity=2)
