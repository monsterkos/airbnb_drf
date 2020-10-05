import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from rooms.serializers import RoomSerializer
from rooms.models import Room
from .models import User
from .serializers import UserSerializer
from .permissions import IsSelf

# from rest_framework.permissions import IsAuthenticated
# from rest_framework.views import APIView


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "list":
            permission_classes = [IsAdminUser]
        elif (
            self.action == "create"
            or self.action == "retrieve"
            or self.action == "favs"
        ):
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsSelf]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=["POST"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if user is not None:
            encoded_jwt = jwt.encode(
                {"pk": user.pk}, settings.SECRET_KEY, algorithm="HS256"
            )
            return Response(data={"token": encoded_jwt, "id": user.pk})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    # users/pk 경로에서 작동하는 경우 detail=True
    @action(detail=True)
    def favs(self, request, pk):
        user = self.get_object()
        serializer = RoomSerializer(user.favs.all(), many=True)
        return Response(serializer.data)

    # 기본 get method 만 정의된 favs 메소드를 확장함
    @favs.mapping.put
    def toggle_favs(self, request, pk):
        pk = request.data.get("pk", None)
        user = self.get_object()
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()
            except Room.DoesNotExist:
                pass
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# class UsersView(APIView):
#     def post(self, request):
#         serializer = UserSerializer(request.data)
#         if serializer.is_valid():
#             new_user = serializer.save()
#             return Response(UserSerializer(new_user))
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class MeView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         return Response(UserSerializer(request.user).data)

#     def put(self, request):
#         serializer = UserSerializer(request.user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response()
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["GET"])
# def user_detail(request, pk):
#     try:
#         user = User.objects.get(pk=pk)
#         return Response(UserSerializer(user).data)
#     except User.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)