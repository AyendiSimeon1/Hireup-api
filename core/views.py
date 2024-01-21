from django.http import HttpResponse
from django.shortcuts import get_object_or_404

import tempfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from rest_framework.decorators import api_view
#from weasyprint import HTML
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import PersonalInformation, Education, WorkExperience, Skill, Project, ResumeTemplate
from .serializers import (
    PersonalInformationSerializer,
    EducationSerializer,
    WorkExperienceSerializer,
    SkillSerializer,
    ProjectSerializer,
    ResumeTemplateSerializer,
)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        
        data = {'message': 'GET request is not typically used for registration.'}
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(request)
            return Response({'user_id': user.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'User logged in successfully'}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class Profile(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    #permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retrieve the profile of the currently logged-in user
        return self.request.user


class PersonalInformationViewSet(viewsets.ModelViewSet):
    queryset = PersonalInformation.objects.all()
    serializer_class = PersonalInformationSerializer

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

class WorkExperienceViewSet(viewsets.ModelViewSet):
    queryset = WorkExperience.objects.all()
    serializer_class = WorkExperienceSerializer

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

from rest_framework.authtoken.models import Token

# def login_view(request):
#     # ... your login logic
#     token, created = Token.objects.get_or_create(user=user)
#     return Response({'token': token.key})

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated

# class ResumeCreateView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
        # ... handle resume creation


class ResumeTemplateList(APIView):

    def get(self, request, format=None):
        template_id = 1
        user_id = 1
        template = get_object_or_404(ResumeTemplate, pk=template_id)
        user_profile = get_object_or_404(User, pk=user_id)

        # Create a PDF file
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

        # Create PDF using ReportLab
        document = canvas.Canvas(response, pagesize=letter)

        # Set the font and draw dynamic text from the database
        document.setFont("Helvetica", 12)
        document.drawString(100, 750, f"Resume Template: {template.name}")
        document.drawString(100, 730, f"Name: {user_profile.email}")
        document.drawString(100, 710, f"Date: {user_profile.username}")

        # Add more dynamic content or flowables as needed

        # Save the PDF
        document.save()

        
        return Response({"message": "PDF generated"})
    