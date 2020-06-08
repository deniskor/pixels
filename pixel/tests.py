import json

from django.test import TestCase, Client

from .models import Pixel
from .forms import WIDTH, HEIGHT


# Create your tests here.
class PixelViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.pixel = Pixel.objects.create(x=1, y=1, color='aaaaaa')

    # ----------- GET ------------
    def test_get_color_success(self):
        resp = self.client.get('', {'x': '1', 'y': '1'})
        json_data = json.dumps({'result': 'ok',
                                'x': self.pixel.x,
                                'y': self.pixel.y,
                                'color': self.pixel.color})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_get_color_default_color_success(self):
        resp = self.client.get('', {'x': '1', 'y': '10'})
        json_data = json.dumps({'result': 'ok', 'x': 1, 'y': 10, 'color': 'ffffff'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_get_color_invalid_data(self):
        # Less than 1
        resp = self.client.get('', {'x': '-1', 'y': '1'})
        json_data = json.dumps({'result': 'error', 'msg': 'invalid data'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        # More than HEIGHT
        resp = self.client.get('', {'x': '1', 'y': str(WIDTH+10)})
        json_data = json.dumps({'result': 'error', 'msg': 'invalid data'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    # ----------- SET ------------
    def test_set_color_success(self):
        resp = self.client.post('', {'x': '2', 'y': '2', 'color': 'bbbbbb'})
        json_data = json.dumps({'result': 'ok', 'msg': 'pixel created',
                                'pixel': {'x': 2, 'y': 2, 'color': 'bbbbbb'}})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_set_color_updated(self):
        resp = self.client.post('', {'x': '1', 'y': '1', 'color': 'bbbbbb'})
        json_data = json.dumps({'result': 'ok', 'msg': 'pixel updated',
                                'pixel': {'x': 1, 'y': 1, 'color': 'bbbbbb'}})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_set_color_invalid_data(self):
        msg = 'invalid data'
        # Less than 1
        resp = self.client.post('', {'x': '0', 'y': '1', 'color': 'aaaaaa'})
        json_data = json.dumps({'result': 'error', 'msg': msg})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        # More than 20
        resp = self.client.post('', {'x': '0', 'y': str(WIDTH+10), 'color': 'aaaaaa'})
        json_data = json.dumps({'result': 'error', 'msg': msg})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        # Without color
        resp = self.client.post('', {'x': '1', 'y': '1'})
        json_data = json.dumps({'result': 'error', 'msg': msg})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        # Invalid color len>6
        resp = self.client.post('', {'x': '2', 'y': '2', 'color': 'bb1bggg'})
        json_data = json.dumps({'result': 'error', 'msg': msg})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        # Invalid color out of 0-9A-F
        resp = self.client.post('', {'x': '2', 'y': '2', 'color': 'xYZw13'})
        json_data = json.dumps({'result': 'error', 'msg': msg})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_delete_color_invalid_data(self):
        msg = 'invalid data'
        # Less than 1
        resp = self.client.delete('', json.dumps({'x': '-1', 'y': '1'}))
        json_data = json.dumps({'result': 'error', 'msg': msg})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        # More than 20
        resp = self.client.delete('', json.dumps({'x': '0', 'y': '21'}))
        json_data = json.dumps({'result': 'error', 'msg': msg})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_delete_color_success(self):
        resp = self.client.delete('', json.dumps({'x': '1', 'y': '1'}))
        json_data = json.dumps({'result': 'ok', 'msg': 'pixel deleted'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_delete_color_nothing_to_delete(self):
        resp = self.client.delete('', json.dumps({'x': '2', 'y': '1'}))
        json_data = json.dumps({'result': 'error', 'msg': 'nothing to delete'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))