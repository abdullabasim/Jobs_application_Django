from django.shortcuts import render
from rest_framework.decorators import api_view ,permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializersData import SignUpSerializer ,UserInfoSerializer
from django.shortcuts import get_object_or_404
from rest_framework import  status

from rest_framework.permissions import IsAuthenticated
from .validators import validate_file_extension
# Create your views here.

@api_view(['POST'])
def register(request) :
    data = request.data
    serializer = SignUpSerializer(data =data)

    if serializer.is_valid() :
        serializer.save()

        return Response(
                {'message': 'The user register done'},
                status=status.HTTP_200_OK
            )
    else :
        return Response(serializer.errors)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def currentUser(request):

    serializer = UserInfoSerializer(request.user,many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUser(request):

    user = request.user
    serializer = SignUpSerializer(user,data=request.data,many=False)
    if serializer.is_valid():
         serializer.save()
         return Response(serializer.data)

    else:
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def uploadResume(request):

    user = request.user
    resume = request.FILES['resume']

    if resume == '' :
        return Response({"ERROR" : "Please upload your resume"},status=status.HTTP_400_BAD_REQUEST)

    isValidFile = validate_file_extension(resume.name)

    if not isValidFile :
        return Response({"ERROR" : "Please upload your resume with extension pdf"},status=status.HTTP_400_BAD_REQUEST)

    user.userprofile.resume = resume
    user.userprofile.save()
    serializer = UserInfoSerializer(user,context={'request': request}, many=False)
    return Response(serializer.data)