import unittest
from run import app


def hasindex(lst, idx):
    ln = len(lst)
    return (abs(idx) < ln) or (idx == -ln)


class TailsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.testing = True
        cls.test_client = app.test_client()

    def test_get_all(self):
        response = self.test_client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['results']), 95)

    def test_lookup_partial_postcode_1(self):
        """
        Lookup postcode or partial postcode.
        """
        response = self.test_client.get('/?postcode=SW11')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['results']), 1)

    def test_lookup_partial_postcode_2(self):
        """
        Lookup postcode or partial postcode.
        """
        response = self.test_client.get('/?postcode=GU')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['results']), 6)

    def test_lookup_postcode_radius_01(self):
        """
        Lookup nearby stores based on exact match of `postcode` and
        a small `radius` parameter.
        """
        response = self.test_client.get('/?nearby=NW1+9EX&radius=0.1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['results']), 4)

    def test_lookup_postcode_default_radius_high_density(self):
        """
        Lookup nearby stores based on exact match of `postcode` and
        the default radius param, in a high density area - Camden.
        """
        response = self.test_client.get('/?nearby=NW1+9EX')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['results']), 23)

    def test_lookup_postcode_default_radius_lower_density(self):
        """
        Lookup nearby stores based on exact match of `postcode` and
        the default radius param, in a lower density area.
        """
        response = self.test_client.get('/?nearby=SG13+7RQ')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['results']), 7)

    def test_lookup_postcode_radius_north_to_south(self):
        """
        Check if postcodes are ordered north to south.
        """
        response = self.test_client.get('/?nearby=NW1+9EX')
        latitudes = [e['latitude'] for e in response.json['results']]

        idx_latitudes = enumerate(latitudes)
        next(idx_latitudes)

        for idx, lat in idx_latitudes:
            self.assertTrue(lat > latitudes[idx - 1])

    def test_nearby_bogus_postcode(self):
        response = self.test_client.get('/?nearby=NW3+XYZ')
        self.assertEqual(response.status_code, 400)

    def test_nearby_bogus_radius(self):
        response = self.test_client.get('/?nearby=NW1+9EX&radius=bogus')
        self.assertEqual(response.status_code, 422)


if __name__ == '__main__':
    unittest.main(verbosity=2)
