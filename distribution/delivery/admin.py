from django.contrib import admin
from .models import Delivery, DeliveryStatus, Transport

# Register your models here.


class StatusAdmin(admin.ModelAdmin):
    list_display = ["code", "name"]
    readonly_fields = ["created_at", "code", "updated_at", "created_by", "updated_by"]
    # fields = ['code', 'name', 'description', 'created_at', 'updated_at']


admin.site.register(Delivery)
admin.site.register(DeliveryStatus)
admin.site.register(Transport)

# from django.contrib.auth import authenticate
# from rest_framework.authtoken.models import Token
# from rest_framework.decorators import api_view
# from rest_framework.response import Response

# @api_view(['POST'])
# def login(request):
#     username = request.data.get('username')
#     password = request.data.get('password')
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})
#     else:
#         return Response({'error': 'Invalid credentials'})
