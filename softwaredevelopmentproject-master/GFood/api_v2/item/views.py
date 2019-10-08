from django.http import HttpResponse

def start(request):
    return HttpResponse(status=200)

# from rest_framework import status
# from rest_framework.response import Response
# def start(self):
#     content = {'please move along': 'nothing to see here'}
#     return Response(content, status=status.HTTP_404_NOT_FOUND)