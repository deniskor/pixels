from .models import Pixel
from django.http import JsonResponse
import re, json
from django.http import QueryDict

def validate_color(color):
    if len(color) == 6 and re.match(r'^[0-9a-fA-F]{6}$', color):
        return True
    return False

def validate_coords(x, y):
    if 0 < x <= 20 and 0 < y <= 20:
        return True
    return False

# Create your views here.
def index(request):
    pass


def get_color(request):
    if request.method == 'GET':
        x = int(request.GET.get('x', 0))
        y = int(request.GET.get('y', 0))

        if validate_coords(x, y):
            pixel = Pixel.objects.filter(x__exact=x, y__exact=y).first()
            if not pixel:
                pixel = Pixel(x=x, y=y)
            resp = {'result': 'ok', 'x': pixel.x, 'y': pixel.y, 'color': pixel.color}
        else:
            resp = {'result': 'error', 'msg': 'not valid coords'}
        return JsonResponse(resp)
    else:
        resp = {'result': 'error', 'msg': 'not allowed method'}
        return JsonResponse(resp)


def change_color(request):
    if request.method == 'PUT':
        PUT = json.loads(request.body)

        x = int(PUT.get('x', 0))
        y = int(PUT.get('y', 0))
        color = PUT.get('color')

        if validate_coords(x, y):
            pixel = Pixel.objects.filter(x__exact=x, y__exact=y).first()
            if not validate_color(color):
                resp = {'result': 'error', 'msg': 'not valid color'}
            elif not pixel:
                resp = {'result': 'error', 'msg': 'pixel not created'}
            elif pixel.color == color:
                resp = {'result': 'error', 'msg': 'the same color'}
            else:
                pixel.color = color
                pixel.save()
                resp = {'result': 'ok', 'msg': 'pixel changed',
                        'pixel': {'x': pixel.x, 'y': pixel.y, 'color': pixel.color}}
        else:
            resp = {'result': 'error', 'msg': 'not valid coords'}
        return JsonResponse(resp)
    else:
        resp = {'result': 'error', 'msg': 'not allowed method'}
        return JsonResponse(resp)


def delete_color(request):
    if request.method == 'DELETE':
        DELETE = json.loads(request.body)

        x = int(DELETE.get('x', 0))
        y = int(DELETE.get('y', 0))
        if validate_coords(x, y):
            pixel = Pixel.objects.filter(x__exact=x, y__exact=y).first()
            if pixel:
                pixel.delete()
                resp = {'result': 'ok', 'msg': 'pixel deleted'}
            else:
                resp = {'result': 'error', 'msg': 'nothing to delete'}
        else:
            resp = {'result': 'error', 'msg': 'not valid coords'}
        return JsonResponse(resp)
    else:
        resp = {'result': 'error', 'msg': 'not allowed method'}
        return JsonResponse(resp)


def set_color(request):
    if request.method == 'POST':
        x = int(request.POST.get('x', 0))
        y = int(request.POST.get('y', 0))
        color = request.POST.get('color')

        if 0 < x <= 20 and 0 < y <= 20:
            pixel = Pixel.objects.filter(x__exact=x, y__exact=y).first()
            if not validate_color(color):
                resp = {'result': 'error', 'msg': 'not valid color'}
            elif not pixel:
                pixel = Pixel.objects.create(x=x, y=y, color=color)
                resp = {'result': 'ok', 'msg': 'pixel created',
                        'pixel': {'x': pixel.x, 'y': pixel.y, 'color': pixel.color}}
            else:
                resp = {'result': 'error', 'msg': 'pixel was created before'}
        else:
            resp = {'result': 'error', 'msg': 'not valid coords'}

        return JsonResponse(resp)
    else:
        resp = {'result': 'error', 'msg': 'not allowed method'}
        return JsonResponse(resp)


