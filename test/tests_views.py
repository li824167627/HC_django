from django.test import TestCase

class TestViews(TestCase):
    def test_index_view(self):
        response = self.client.get("http://127.0.0.1:8000/api/show_time?show_time='10.100.19.228'")
        print(response)