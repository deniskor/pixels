from .models import Pixel
from django.http import JsonResponse
import json
from django.views import View
from .forms import PixelForm, PixelPOSTForm


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




