import json

from django.test import TestCase, Client

from .models import Pixel


# Create your tests here.
class PixelViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.pixel = Pixel.objects.create(x=1, y=1, color='aaaaaa')

    def test_get_color_success(self):
        resp = self.client.get('/get', {'x': '1', 'y': '1'})
        json_data = json.dumps({'result': 'ok',
                                'x': self.pixel.x,
                                'y': self.pixel.y,
                                'color': self.pixel.color})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_get_color_default_color_success(self):
        resp = self.client.get('/get', {'x': '1', 'y': '10'})
        json_data = json.dumps({'result': 'ok', 'x': 1, 'y': 10, 'color': 'ffffff'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_get_color_not_GET_method(self):
        resp = self.client.post('/get', {'x': '1', 'y': '1'})
        json_data = json.dumps({'result': 'error', 'msg': 'not allowed method'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        resp = self.client.put('/get', {'x': '1', 'y': '1'})
        json_data = json.dumps({'result': 'error', 'msg': 'not allowed method'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        resp = self.client.delete('/get', {'x': '1', 'y': '1'})
        json_data = json.dumps({'result': 'error', 'msg': 'not allowed method'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_get_color_not_valid_coords(self):
        # Less than 1
        resp = self.client.get('/get', {'x': '-1', 'y': '1'})
        json_data = json.dumps({'result': 'error', 'msg': 'not valid coords'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        # More than 20
        resp = self.client.get('/get', {'x': '1', 'y': '21'})
        json_data = json.dumps({'result': 'error', 'msg': 'not valid coords'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_set_color_not_POST_method(self):
        resp = self.client.get('/set', {'x': '1', 'y': '1', 'color': 'bbbbbb'})
        json_data = json.dumps({'result': 'error', 'msg': 'not allowed method'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        resp = self.client.put('/set', {'x': '1', 'y': '1', 'color': 'bbbbbb'})
        json_data = json.dumps({'result': 'error', 'msg': 'not allowed method'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        resp = self.client.delete('/set', {'x': '1', 'y': '1', 'color': 'bbbbbb'})
        json_data = json.dumps({'result': 'error', 'msg': 'not allowed method'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_set_color_success(self):
        resp = self.client.post('/set', {'x': '2', 'y': '2', 'color': 'bbbbbb'})
        json_data = json.dumps({'result': 'ok', 'msg': 'pixel created',
                                'pixel': {'x': 2, 'y': 2, 'color': 'bbbbbb'}})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_set_color_already_exists(self):
        resp = self.client.post('/set', {'x': '1', 'y': '1', 'color': 'aaaaaa'})
        json_data = json.dumps({'result': 'error', 'msg': 'pixel was created before'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_set_color_not_valid_coords(self):
        # Less than 1
        resp = self.client.post('/set', {'x': '0', 'y': '1', 'color': 'aaaaaa'})
        json_data = json.dumps({'result': 'error', 'msg': 'not valid coords'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        # More than 20
        resp = self.client.post('/set', {'x': '0', 'y': '21', 'color': 'aaaaaa'})
        json_data = json.dumps({'result': 'error', 'msg': 'not valid coords'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_set_color_not_valid_color(self):
        resp = self.client.post('/set', {'x': '2', 'y': '2', 'color': 'bb1bggg'})
        json_data = json.dumps({'result': 'error', 'msg': 'not valid color'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        resp = self.client.post('/set', {'x': '2', 'y': '2', 'color': 'xYZw13'})
        json_data = json.dumps({'result': 'error', 'msg': 'not valid color'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_change_color_not_PUT_method(self):
        resp = self.client.get('/put', {'x': '1', 'y': '1', 'color': 'bbbbbb'})
        json_data = json.dumps({'result': 'error', 'msg': 'not allowed method'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        resp = self.client.post('/put', {'x': '1', 'y': '1', 'color': 'bbbbbb'})
        json_data = json.dumps({'result': 'error', 'msg': 'not allowed method'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        resp = self.client.delete('/put', {'x': '1', 'y': '1', 'color': 'bbbbbb'})
        json_data = json.dumps({'result': 'error', 'msg': 'not allowed method'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_change_color_not_valid_color(self):
        resp = self.client.put('/put', json.dumps({'x': '1', 'y': '1', 'color': 'bb1bggg'}))
        json_data = json.dumps({'result': 'error', 'msg': 'not valid color'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        resp = self.client.put('/put', json.dumps({'x': '2', 'y': '2', 'color': 'xYZw13'}))
        json_data = json.dumps({'result': 'error', 'msg': 'not valid color'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_change_color_success(self):
        resp = self.client.put('/put', json.dumps({'x': '1', 'y': '1', 'color': 'bbbb11'}))
        json_data = json.dumps({'result': 'ok', 'msg': 'pixel changed',
                                'pixel': {'x': 1, 'y': 1, 'color': 'bbbb11'}})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_change_color_nothing_to_change(self):
        resp = self.client.put('/put', json.dumps({'x': '1', 'y': '1', 'color': 'aaaaaa'}))
        json_data = json.dumps({'result': 'error', 'msg': 'the same color'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_change_color_pixel_not_created(self):
        resp = self.client.put('/put', json.dumps({'x': '2', 'y': '1', 'color': 'aaaaaa'}))
        json_data = json.dumps({'result': 'error', 'msg': 'pixel not created'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_change_color_not_valid_coords(self):
        # Less than 1
        resp = self.client.put('/put', json.dumps({'x': '-1', 'y': '1', 'color': 'aaaaaa'}))
        json_data = json.dumps({'result': 'error', 'msg': 'not valid coords'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        # More than 20
        resp = self.client.put('/put', json.dumps({'x': '0', 'y': '21', 'color': 'aaaaaa'}))
        json_data = json.dumps({'result': 'error', 'msg': 'not valid coords'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_delete_color_not_DELETE_method(self):
        resp = self.client.get('/del', {'x': '1', 'y': '1'})
        json_data = json.dumps({'result': 'error', 'msg': 'not allowed method'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        resp = self.client.post('/del', {'x': '1', 'y': '1'})
        json_data = json.dumps({'result': 'error', 'msg': 'not allowed method'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        resp = self.client.put('/del', {'x': '1', 'y': '1'})
        json_data = json.dumps({'result': 'error', 'msg': 'not allowed method'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_delete_color_not_valid_coords(self):
        # Less than 1
        resp = self.client.delete('/del', json.dumps({'x': '-1', 'y': '1'}))
        json_data = json.dumps({'result': 'error', 'msg': 'not valid coords'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

        # More than 20
        resp = self.client.delete('/del', json.dumps({'x': '0', 'y': '21'}))
        json_data = json.dumps({'result': 'error', 'msg': 'not valid coords'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_delete_color_success(self):
        resp = self.client.delete('/del', json.dumps({'x': '1', 'y': '1'}))
        json_data = json.dumps({'result': 'ok', 'msg': 'pixel deleted'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_delete_color_nothing_to_delete(self):
        resp = self.client.delete('/del', json.dumps({'x': '2', 'y': '1'}))
        json_data = json.dumps({'result': 'error', 'msg': 'nothing to delete'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))