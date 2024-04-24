
from django.http import HttpResponse, JsonResponse
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import pdfkit
import tempfile
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from django.contrib.auth import authenticate, login

from .serializers import RegisterSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import viewsets
from rest_framework.decorators import api_view
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import PersonalInformation, Education, ProfessionalExperience, Skill, Project, ResumeTemplate, TemplateSelection

from core.models import User
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from io import BytesIO
import base64

from .serializers import (
    PersonalInformationSerializer,
    EducationSerializer,
    ProfessionalExperienceSerializer,
    SkillSerializer,
    ProjectSerializer,
    ResumeTemplateSerializer,
    ProfileSerializer,
    TemplateSelectionSerializer,
    SocialsSerializer
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
        serializer = ProfileSerializer()
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            serializer = ProfileSerializer(user)
            return Response({
                'message': 'User logged in successfully',
                'user': serializer.data
            }, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class Profile(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ProfileSerializer
    #permission_classes = [IsAuthenticated]

    def get_object(self):
        
        return self.request.user


class PersonalInformationViewSet(viewsets.ModelViewSet):
    queryset = PersonalInformation.objects.all()
    serializer_class = PersonalInformationSerializer

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

class ProfessionalExperienceViewSet(viewsets.ModelViewSet):
    queryset = ProfessionalExperience.objects.all()
    serializer_class = ProfessionalExperienceSerializer

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer




class ResumeTemplateList(APIView):
    
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user 
        print(user_id)
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        information = PersonalInformation.objects.filter(user=user)  # Filter by user
        experiences = ProfessionalExperience.objects.filter(user=user)  # Filter by user
        skills = Skill.objects.filter(user=user)  # Filter by user
        projects = Project.objects.filter(user=user)  # Filter by user

        template_id = 1
        if not template_id:
            return Response({"error": "Missing template ID"}, status=400)

        try:
            html_template = ResumeTemplate.objects.get(pk=template_id)
        except ResumeTemplate.DoesNotExist:
            return Response({"error": "Template not found"}, status=404)

        skills_string = ', '.join([str(skill) for skill in skills])

        # Consider using a templating engine instead of manual string formatting
        html_content = html_template.content.format(
            user=user,
            information=information,  # Include personal information
            experiences=experiences,  # Include experiences
            skills=skills_string,
            projects=projects,
        )

        # PDF generation (assuming wkhtmltopdf is installed and configured)
        try:
            path_wkhtmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'
            config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            pdf = pdfkit.from_string(html_content, configuration=config)
            response = Response(pdf, content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
            return response
        except Exception as e:
            print(f"Error generating PDF: {e}")  # Log the error for debugging





def generate_pdf(context, template_name='pdf_template.html'):
    html_content = render_to_string(template_name, context)
    result = BytesIO()
    pisa.CreatePDF(html_content, dest=result)
    
    # Check if PDF generation was successful
    if not result:
        raise Exception("PDF generation failed.")
    
    # Return the generated PDF as a binary object
    return result.getvalue()

class GeneratePDFAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            
        
            access_token = request.headers.get("Authorization").split()[1] 
            

            # if not user.is_authenticated:
            #     raise HTTP_401_UNAUTHORIZED
            template_id = 1
            
            # user_info = PersonalInformation.objects.filter(user=user)
            # experiences = ProfessionalExperience.objects.filter(user_id=user)
            # educations = Education.objects.filter(user_id=user)
            # projects = Project.objects.filter(user_id=user)
            # socials = Socials.objects.filter(user_id=user)
            # professional_summary = ProfessionalSummary.objects.filter(user_id=user)
            # user_info = user.personal_info.all()
                             
            # experience  = user.ProfessionalExperience.all()
            # educations = user.Education.all()
            # socials = user.Socials.all()
            # professional_summary =  user.ProfessionalSummary.all()
            # projects = user.Project.all()

            #user_info = user.personal_info
            #educations = user.educations.all()

            user = get_object_or_404(User, id=1)
            socials = user.socials
            professional_summary = user.professional_summary
            projects = user.projects.all()
           
            #template = ResumeTemplate.objects.get(id=template_id)

            # user_info_serializer = PersonalInformationSerializer(user_info)
            # experience_serializer = ProfessionalExperienceSerializer(experiences, many=True)
            # education_serializer = EducationSerializer(educations, many=True)
            project_serializer = ProjectSerializer(projects, many=True)
            socials_serializer = SocialsSerializer(socials)
            professional_summary_serializer = ProfessionalExperienceSerializer(professional_summary)
  
            context = {
    #             'user_info': user_info_serializer.data,
    #             'experiences': experience_serializer.data,
    #             'educations': education_serializer.data,
                'projects': project_serializer.data,
                'socials': socials_serializer.data,
                'professional_summary': professional_summary_serializer.data,
    #             'template_content': template.content
             }
            

            pdf_content = generate_pdf(context)

            # Return the PDF as a downloadable file
            response = Response({
                'pdf_file': base64.b64encode(pdf_content).decode()  # Encode the binary content to base64
            }, status=status.HTTP_200_OK)
            
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
   