import json

from django.http import JsonResponse
from django.views import View

from .forms import PixelForm, PixelPOSTForm, RectangleForm
from .models import Pixel, Rectangle


class PixelView(View):
    def get(self, request):
        form = PixelForm(request.GET)
        if form.is_valid():
            rect = form.cleaned_data.get('rect')
            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            pixel = Pixel.objects.filter(x__exact=x, y__exact=y, rect=rect).first()
            if not pixel:
                pixel = Pixel(x=x, y=y, rect=rect)
            resp = {'result': 'ok', 'rect': pixel.rect.id, 'x': pixel.x, 'y': pixel.y, 'color': pixel.color}
        else:
            resp = {'result': 'error', 'msg': 'invalid data'}
        return JsonResponse(resp)

    def post(self, request):
        form = PixelPOSTForm(request.POST)
        if form.is_valid():
            rect = form.cleaned_data.get('rect')
            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')
            color = form.cleaned_data.get('color')

            pixel, c = Pixel.objects.update_or_create(x=x, y=y, rect=rect, defaults={'color': color})

            resp = {'result': 'ok', 'msg': f'pixel {"created" if c else "updated"}',
                    'pixel': {'rect': pixel.rect.id, 'x': pixel.x, 'y': pixel.y, 'color': pixel.color}}
        else:
            resp = {'result': 'error', 'msg': 'invalid data'}
        return JsonResponse(resp)

    def delete(self, request):
        form = PixelForm(json.loads(request.body))
        if form.is_valid():
            rect = form.cleaned_data.get('rect')
            x = form.cleaned_data.get('x')
            y = form.cleaned_data.get('y')

            pixel = Pixel.objects.filter(x__exact=x, y__exact=y, rect=rect).first()
            if pixel:
                pixel.delete()
                resp = {'result': 'ok', 'msg': 'pixel deleted'}
            else:
                resp = {'result': 'error', 'msg': 'nothing to delete'}
        else:
            resp = {'result': 'error', 'msg': 'invalid data'}

        return JsonResponse(resp)


class RectangleView(View):
    def get(self, request, rect_id=None):
        if not rect_id:
            json_data = [{'id': r.id,
                          'width': r.width,
                          'height': r.height,
                          'pixels': Pixel.objects.filter(rect_id=r.id).count()} for r in Rectangle.objects.all()]
            resp = {'result': 'ok', 'rects': json.dumps(json_data)}
        else:
            try:
                rect = Rectangle.objects.get(id=rect_id)
            except Rectangle.DoesNotExist:
                rect = None
            if rect:
                resp = {'result': 'ok', 'rect_data': json.dumps({'id': rect.id,
                                                                 'width': rect.width,
                                                                 'height': rect.height,
                                                                 'pixels': Pixel.objects.filter(
                                                                     rect_id=rect.id).count()})}
            else:
                resp = {'result': 'error', 'msg': 'invalid data'}
        return JsonResponse(resp)

    def post(self, request):
        form = RectangleForm(request.POST)
        if form.is_valid():
            width = form.cleaned_data.get('width')
            height = form.cleaned_data.get('height')

            rect = Rectangle.objects.create(width=width, height=height)

            resp = {'result': 'ok', 'msg': 'rectangle created',
                    'rect': {'id': rect.id, 'width': rect.width, 'height': rect.height}}
        else:
            resp = {'result': 'error', 'msg': 'invalid data'}
        return JsonResponse(resp)

    def delete(self, request, rect_id=None):
        if rect_id:
            try:
                rect = Rectangle.objects.get(id=rect_id)
            except Rectangle.DoesNotExist:
                rect = None

            if rect:
                rect.delete()
                resp = {'result': 'ok', 'msg': 'rectangle deleted'}
            else:
                resp = {'result': 'error', 'msg': 'nothing to delete'}
        else:
            resp = {'result': 'error', 'msg': 'invalid data'}

        return JsonResponse(resp)

    #from django.utils.decorators import method_decorator
    # from django.views.decorators.csrf import csrf_exempt
    #
    # @method_decorator(csrf_exempt)
    # def dispatch(self, request, *args, **kwargs):
    #     return super(RectangleView, self).dispatch(request, *args, **kwargs)