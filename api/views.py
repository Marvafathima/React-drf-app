from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics,permissions,viewsets
from django.contrib.auth.models import User
from base.models import Profile
from .serializer import RegistrationSerializer,ProfileSerializer,UserSerializer


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.parsers import MultiPartParser,FormParser
from django.db.models import Q

def search_user(request,key):
    
    print("Keyyyy",key)
    try:
        users = User.objects.all()
        if key:
            users=users.filter(Q(username__icontains =key) | Q(first_name__icontains =key))
        else:
            print("key is empty")
        print(users)
        
        
        serializer = UserSerializer(users, many=True)
        print(serializer.data)
        print("SUCCESS SERACHING BACK END")
        
        return JsonResponse(serializer.data,safe=False)
    except Exception as e:
        print("ERROR SERACHING BACK END")
        return JsonResponse({'error':str(e)})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class= UserSerializer
    permission_classes=[permissions.IsAdminUser]

class UpdateProfileImageView(generics.UpdateAPIView):
    permission_classes= [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer
    parser_classes=[MultiPartParser,FormParser]

    def get_object(self):

        return self.request.user.profile

class UserProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        user = self.request.user
        if not hasattr(user, 'profile'):
            user.profile = Profile.objects.create(user=user)
        return user.profile

    def get(self, request, *args, **kwargs):
        profile = self.get_object()
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

class RegisterView(generics.CreateAPIView):
    queryset= User.objects.all()
    serializer_class= RegistrationSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['provider'] = 'kino'
        token['is_superuser'] = user.is_superuser
        # ...
        print("user",user.is_superuser)
        return token
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def getRoutes(request):
    routs=[
        'api/token',
        'api/token/refresh',
        'api/register'
    ]

    return Response(routs)