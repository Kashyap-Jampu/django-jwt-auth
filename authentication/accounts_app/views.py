from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
# {"email": "user1@gmail.com","password": "12345"}

from .models import User

# Create your views here.
def home(request):
    return render(request,'home.html')
@api_view(["POST"])
def register(request):
    if request.method=='POST':
        serializer=UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def see(request):
    if request.method=='GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

@api_view(["POST"])
def login_view(request):
    if request.method=="POST":
        email=request.data["email"]
        password=request.data["password"]
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('user not found')
        if not user.check_password(password):
            raise AuthenticationFailed('incorreect password')
        payload={
        "id":user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=5),
        "iat": datetime.datetime.utcnow()
        }
        token =jwt.encode(payload,"secrect",algorithm='HS256')
        response=Response()
        response.set_cookie(key="jwt" , value=token, httponly=True)
        response.data={"jwt" :token}
        return response


@api_view(["GET","POST"])
def user_view(request):
    if request.method=="GET":
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('please login')
        try:
            payload=jwt.decode(token,'secrect', algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('time out')
        user=User.objects.get(id=payload["id"])
        serializer=UserSerializer(user)
        return Response(serializer.data)
    elif request.method=="POST":
        token=request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('please login')
        try:
            payload=jwt.decode(token,'secrect', algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('time out')
        user=User.objects.get(id=payload["id"])
        item=request.data["item"]
        item_content=request.data["item_data"]
        if item=="email":
            if User.filter(email=item_content).exists():
                return Response("email already in use")
        elif item=="username":
            user.username=item_content
            user.save()
            return Response("added succesfully")
        elif item=="address":
            user.address=item_content
            user.save()
            return Response("added succesfully")






@api_view(["GET"])
def logout(request):
    response=Response()
    response.delete_cookie('jwt')
    response.data={
    "messsage " :"success"
    }
    return response
def register_d(request):
    return render(request,"register.html")
def first_page(request):
    return render(request,"first_page.html")
