from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from apps.users.models import UserSerializer, User
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import CreateAPIView
from rest_framework.pagination import PageNumberPagination


# Create your views here.
class UserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        users = User.objects.all()

        paginator = PageNumberPagination()
        paginator.page_size = 10

        result_page = paginator.paginate_queryset(users, request)

        users_serializer = UserSerializer(result_page, many=True)

        return Response({
            "ok": True,
            "result": paginator.get_paginated_response(users_serializer.data).data
        }, status=status.HTTP_200_OK)


@api_view(['DELETE', 'PUT', 'GET'])
@csrf_exempt
def manage_user(request, id):
    try:
        user = User.objects.get(id=id)
    except User.DoesNotExist:
        return Response({
            "ok": False,
            "result": f"User does not exist (id = {id})"
        }, status=status.HTTP_404_NOT_FOUND)
    print(f'ID: ${request.data}')
    if request.method == 'DELETE':
        user.delete()
        return Response({
            "ok": True,
            "result": "User deleted"
        }, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        user_serializer = UserSerializer(user, data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({
                "ok": True,
                "result": user_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            'ok': False,
            'result': user_serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        user_serializer = UserSerializer(user)
        return Response({
            "ok": True,
            'result': user_serializer.data
        }, status=status.HTTP_200_OK)
