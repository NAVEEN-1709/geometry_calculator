import unittest

from app import app


class GeometryAppTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_remaining_shape_pages_render(self):
        routes = [
            "/ellipse",
            "/rhombus",
            "/trapezium",
            "/pentagon",
            "/hexagon",
            "/cube",
            "/cuboid",
            "/cylinder",
            "/cone",
            "/sphere",
        ]

        for route in routes:
            with self.subTest(route=route):
                response = self.client.get(route)
                self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
