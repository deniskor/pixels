import json

from django.test import TestCase, Client

from .models import Pixel, Rectangle


# Create your tests here.
class PixelViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.rect = Rectangle.objects.create()
        cls.pixel = Pixel.objects.create(rect=cls.rect, x=1, y=1, color='aaaaaa')

    # ----------- GET ------------
    def test_get_pixel_success(self):
        response = json.dumps({'result': 'ok',
                               'rect': self.pixel.rect.id,
                               'x': self.pixel.x,
                               'y': self.pixel.y,
                               'color': self.pixel.color})

        resp = self.client.get('', {'rect': '1', 'x': '1', 'y': '1'})
        self.assertEqual(resp.content, response.encode('utf-8'))

    def test_get_pixel_default_color_success(self):
        response = json.dumps({'result': 'ok',
                               'rect': 1,
                               'x': 1,
                               'y': 10,
                               'color': 'ffffff'})

        resp = self.client.get('', {'rect': '1', 'x': '1', 'y': '10', 'color': 'ffffff'})
        self.assertEqual(resp.content, response.encode('utf-8'))

    def test_get_pixel_invalid_data(self):
        response = json.dumps({'result': 'error', 'msg': 'invalid data'})

        # Less than 1
        resp = self.client.get('', {'rect': '1', 'x': '0', 'y': '1'})
        self.assertEqual(resp.content, response.encode('utf-8'))

        # More than HEIGHT
        resp = self.client.get('', {'rect': '1', 'x': '1', 'y': f'{self.rect.height + 10}'})
        self.assertEqual(resp.content, response.encode('utf-8'))

        # Rect doesn't exist
        resp = self.client.get('', {'rect': '10', 'x': '1', 'y': '1'})
        self.assertEqual(resp.content, response.encode('utf-8'))

    # ----------- SET ------------
    def test_set_color_success(self):
        resp = self.client.post('', {'rect': '1', 'x': '2', 'y': '2', 'color': 'bbbbbb'})
        response = json.dumps({'result': 'ok', 'msg': 'pixel created',
                               'pixel': {'rect': 1,
                                         'x': 2,
                                         'y': 2,
                                         'color': 'bbbbbb'}})
        self.assertEqual(resp.content, response.encode('utf-8'))

    def test_set_color_updated(self):
        resp = self.client.post('', {'rect': '1', 'x': '1', 'y': '1', 'color': 'bbbbbb'})
        response = json.dumps({'result': 'ok', 'msg': 'pixel updated',
                               'pixel': {'rect': 1,
                                         'x': 1,
                                         'y': 1,
                                         'color': 'bbbbbb'}})

        self.assertEqual(resp.content, response.encode('utf-8'))

    def test_set_color_invalid_data(self):
        response = json.dumps({'result': 'error', 'msg': 'invalid data'})

        # Less than 1
        resp = self.client.post('', {'rect': '1', 'x': '0', 'y': '1', 'color': 'aaaaaa'})
        self.assertEqual(resp.content, response.encode('utf-8'))

        # More than 20
        resp = self.client.post('', {'rect': '1', 'x': '0', 'y': f'{self.rect.height + 10}', 'color': 'aaaaaa'})
        self.assertEqual(resp.content, response.encode('utf-8'))

        # Without color
        resp = self.client.post('', {'rect': '1', 'x': '1', 'y': '1'})
        self.assertEqual(resp.content, response.encode('utf-8'))

        # Invalid color len>6
        resp = self.client.post('', {'rect': '1', 'x': '2', 'y': '2', 'color': 'bb1bggg'})
        self.assertEqual(resp.content, response.encode('utf-8'))

        # Invalid color out of 0-F
        resp = self.client.post('', {'rect': '1', 'x': '2', 'y': '2', 'color': 'xYZw13'})
        self.assertEqual(resp.content, response.encode('utf-8'))

        # Rect doesn't exist
        resp = self.client.post('', {'rect': '10', 'x': '1', 'y': '1', 'color': 'aaaaaa'})
        self.assertEqual(resp.content, response.encode('utf-8'))

        # Without Rect
        resp = self.client.post('', {'x': '1', 'y': '1', 'color': 'aaaaaa'})
        self.assertEqual(resp.content, response.encode('utf-8'))

    # ----------- DELETE ------------
    def test_delete_pixel_success(self):
        resp = self.client.delete('', json.dumps({'rect': '1', 'x': '1', 'y': '1'}))
        json_data = json.dumps({'result': 'ok', 'msg': 'pixel deleted'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_delete_pixel_invalid_data(self):
        response = json.dumps({'result': 'error', 'msg': 'invalid data'})
        # Less than 1
        resp = self.client.delete('', json.dumps({'rect': '1', 'x': '0', 'y': '1'}))
        self.assertEqual(resp.content, response.encode('utf-8'))

        # More than height
        resp = self.client.delete('', json.dumps({'rect': '1', 'x': '1', 'y': f'{self.rect.height + 10}'}))
        self.assertEqual(resp.content, response.encode('utf-8'))

        # Rect doesn't exist
        resp = self.client.delete('', json.dumps({'rect': '10', 'x': '1', 'y': '1'}))
        self.assertEqual(resp.content, response.encode('utf-8'))

    def test_delete_pixel_nothing_to_delete(self):
        resp = self.client.delete('', json.dumps({'rect': '1', 'x': '2', 'y': '1'}))
        json_data = json.dumps({'result': 'error', 'msg': 'nothing to delete'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    #
    # Rectangle
    #
    def test_get_rectangle_list_success(self):
        resp = self.client.get('/rects/')
        json_data = [{'id': r.id,
                      'width': r.width,
                      'height': r.height,
                      'pixels': Pixel.objects.filter(rect_id=r.id).count()} for r in Rectangle.objects.all()]

        json_data = json.dumps({'result': 'ok', 'rects': json.dumps(json_data)})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_get_rectangle_retrieve_success(self):
        resp = self.client.get('/rects/1')
        json_data = json.dumps({'id': self.rect.id,
                                'width': self.rect.width,
                                'height': self.rect.height,
                                'pixels': Pixel.objects.filter(
                                    rect_id=self.rect.id).count()})

        json_data = json.dumps({'result': 'ok', 'rect_data': json_data})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_get_rectangle_retrieve_not_created(self):
        resp = self.client.get('/rects/10')
        response = json.dumps({'result': 'error', 'msg': 'invalid data'})
        self.assertEqual(resp.content, response.encode('utf-8'))

    def test_delete_rectangle_success(self):
        resp = self.client.delete('/rects/1')
        json_data = json.dumps({'result': 'ok', 'msg': 'rectangle deleted'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_delete_rectangle_nothing_to_delete(self):
        resp = self.client.delete('/rects/10')
        json_data = json.dumps({'result': 'error', 'msg': 'nothing to delete'})
        self.assertEqual(resp.content, json_data.encode('utf-8'))

    def test_delete_rectangle_no_rect_id(self):
        resp = self.client.delete('/rects/')
        response = json.dumps({'result': 'error', 'msg': 'invalid data'})
        self.assertEqual(resp.content, response.encode('utf-8'))

    def test_post_rectangle_success(self):
        resp = self.client.post('/rects/', {'width': '10', 'height': '10'})
        response = json.dumps({'result': 'ok', 'msg': 'rectangle created',
                               'rect': {'id': 2, 'width': 10, 'height': 10}})
        self.assertEqual(resp.content, response.encode('utf-8'))

    def test_delete_rectangle_invalid_data(self):
        resp = self.client.post('/rects/')
        response = json.dumps({'result': 'error', 'msg': 'invalid data'})
        self.assertEqual(resp.content, response.encode('utf-8'))

        resp = self.client.post('/rects/', {'width': '100000', 'height': '10'})
        response = json.dumps({'result': 'error', 'msg': 'invalid data'})
        self.assertEqual(resp.content, response.encode('utf-8'))
