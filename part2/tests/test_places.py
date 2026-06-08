import unittest

from app import create_app


class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_get_places(self):
        response = self.client.get(
            '/api/v1/places/'
        )

        self.assertEqual(
            response.status_code,
            200
        )

    def test_place_not_found(self):
        response = self.client.get(
            '/api/v1/places/fake-id'
        )

        self.assertEqual(
            response.status_code,
            404
        )
