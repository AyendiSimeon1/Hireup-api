
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
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import JWTAuthentication
from rest_framework import viewsets
from rest_framework.decorators import api_view
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import PersonalInformation, Education, ProfessionalExperience, Skill, Project, ResumeTemplate, TemplateSelection
from django.contrib.auth.models import User

from .serializers import (
    PersonalInformationSerializer,
    EducationSerializer,
    ProfessionalExperienceSerializer,
    SkillSerializer,
    ProjectSerializer,
    ResumeTemplateSerializer,
    ProfileSerializer,
    TemplateSelectionSerializer
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


# class get_resume_template(APIView):
#     def get(self, request):
#         templates = ResumeTemplate.objects.all()
#         serializer = ResumeTemplateSerializer(templates, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         try:
#             # Extract data from the request
#             user_id = request.data.get('user_id')
#             template_id = request.data.get('template_id')
            
#             # Fetch user information based on the user ID
#             user_info = PersonalInformation.objects.get(user_id=user_id)
#             experience = Experience.objects.filter(user_id=user_id)
            
#             # Fetch the selected template
#             template = Template.objects.get(id=template_id)
            
#             # Serialize user information and experience
#             user_info_serializer = PersonalInformationSerializer(user_info)
#             experience_serializer = ExperienceSerializer(experience, many=True)
            
#             # Combine user information, experience, and template content
#             context = {
#                 'user_info': user_info_serializer.data,
#                 'experience': experience_serializer.data,
#                 'template_content': template.html_content
#             }
            
#             # Generate PDF
#             pdf_file = generate_pdf(context)
            
#             # Return the PDF file
#             return Response({'pdf_file': pdf_file}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class get_resume_template(APIView):
    def post(self, request):
        # Access the request data
        data = JSONParser().parse(request)  # Optional for raw JSON handling
        selected_template_id = data.get('template_name')

        # Validate and create the template object
        if selected_template_id:
            template_obj, created = TemplateSelection.objects.get_or_create(
                template_name=selected_template_id
            )
            response_data = {'message': 'Template selection successful'}
        else:
            response_data = {'message': 'Please provide a template name'}
            return JsonResponse(response_data, status=400)  # Bad request

        return JsonResponse(response_data, status=200)


# class GeneratePDFAPIView(APIView):
#     def get(self, request):
#         try:
#             # Extract data from the request
#             user_id = request.data.get('user_id')
#             template_id = request.data.get('template_id')
            
#             # Fetch user information based on the user ID
#             user_info = PersonalInformation.objects.get(user_id=user_id)
#             experience = Experience.objects.filter(user_id=user_id)
            
#             # Fetch the selected template
#             template = Template.objects.get(id=template_id)
            
#             # Serialize user information and experience
#             user_info_serializer = PersonalInformationSerializer(user_info)
#             experience_serializer = ExperienceSerializer(experience, many=True)
            
#             # Combine user information, experience, and template content
#             context = {
#                 'user_info': user_info_serializer.data,
#                 'experience': experience_serializer.data,
#                 'template_content': template.html_content
#             }
            
#             # Generate PDF
#             pdf_file = generate_pdf(context)
            
#             # Return the PDF file
#             return Response({'pdf_file': pdf_file}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



class GeneratePDFAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            
            
            user = request.user
            template_id = 1
            
            user_info = PersonalInformation.objects.get(user=user)
            experiences = ProfessionalExperience.objects.filter(user_id=user)
            educations = Education.objects.filter(user_id=user)
            projects = Project.objects.filter(user_id=user)
            socials = Socials.objects.get(user_id=user)
            professional_summary = ProfessionalSummary.objects.get(user_id=user)
            
            # Fetch the selected template
            template = ResumeTemplate.objects.get(id=template_id)

            user_info_serializer = PersonalInformationSerializer(user_info)
            experience_serializer = ProfessionalExperienceSerializer(experiences, many=True)
            education_serializer = EducationSerializer(educations, many=True)
            project_serializer = ProjectSerializer(projects, many=True)
            socials_serializer = SocialsSerializer(socials)
            professional_summary_serializer = ProfessionalSummarySerializer(professional_summary)
  
            context = {
                'user_info': user_info_serializer.data,
                'experiences': experience_serializer.data,
                'educations': education_serializer.data,
                'projects': project_serializer.data,
                'socials': socials_serializer.data,
                'professional_summary': professional_summary_serializer.data,
                'template_content': template.content
            }
            
            # Generate PDF
            pdf_file = self.generate_pdf(context, template)
            
            # Return the PDF file
            return Response({'pdf_file': pdf_file}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def generate_pdf(self, context, template):
        try:
            template = get_template(template)
            html = template.render(context)
            
            pdf_file_path = settings.MEDIA_ROOT + '/resume.pdf'
            with open(pdf_file_path, 'w+b') as pdf_file:
                pisa.CreatePDF(html, dest=pdf_file)
                
            return pdf_file_path
        except Exception as e:
            raise e