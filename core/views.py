
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
from rest_framework import viewsets
from rest_framework.decorators import api_view
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import PersonalInformation, Education, ProfessionalExperience, Skill, Project, ResumeTemplate
from .serializers import (
    PersonalInformationSerializer,
    EducationSerializer,
    ProfessionalExperienceSerializer,
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


# class ResumeTemplateList(APIView):
#     #permission_classes = [IsAuthenticated]
#     def get(self, request):
#         user_id = 1
#         user = request.user
#         user = User.objects.get(pk=user_id)
#         information = PersonalInformation.objects.all()
#         experiences = ProfessionalExperience.objects.all()
#         skills = Skill.objects.filter(user=user)
#         projects = Project.objects.filter(user=user)

#         # data = request.data
#         # template_id = data['templateId']
#         template_id = 2
#         # resume_data = data['resumeData']
#         # Fetch the HTML template from the database
#         skills_string = ', '.join([str(skill) for skill in skills])
#         personal_string = ', '.join([str(personal) for personal in information])

       

#         # Replace the placeholder in the template
        
#         try:
#             html_template = ResumeTemplate.objects.get(pk=template_id)
#         except HtmlTemplate.DoesNotExist:
#             return HttpResponse("Template not found", status=404)
        
      
#         job_titles = ', '.join([experience.job_title for experience in experiences])
#         responsibilities = ', '.join([experience.responsibilities for experience in experiences])

#         #html_content = html_template.design.replace('{experiences}', experiences_html)
#         html_content = html_template.content.format(
#             user=user,
#             information=personal_string,
#             experiences=experiences, 
#             skills=skills_string, 
#             projects=projects, 
#             job_titles=job_titles, 
#             responsibilities=responsibilities
#             )

        
#         path_wkhtmltopdf = r'C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe'  
#         config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

#         pdf = pdfkit.from_string(html_content, configuration=config)

   
#         return HttpResponse(html_content, content_type='text/html')
      
            

#         # response = HttpResponse(pdf, content_type='application/pdf')
#         # response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
#         # return response


class get_resume_template(APIView):
    def get(self, request):
        templates = ResumeTemplate.objects.all()
        serializer = ResumeTemplateSerializer(templates, many=True)
        return Response(serializer.data)

    def post(self, request):
        try:
            # Extract data from the request
            user_id = request.data.get('user_id')
            template_id = request.data.get('template_id')
            
            # Fetch user information based on the user ID
            user_info = PersonalInformation.objects.get(user_id=user_id)
            experience = Experience.objects.filter(user_id=user_id)
            
            # Fetch the selected template
            template = Template.objects.get(id=template_id)
            
            # Serialize user information and experience
            user_info_serializer = PersonalInformationSerializer(user_info)
            experience_serializer = ExperienceSerializer(experience, many=True)
            
            # Combine user information, experience, and template content
            context = {
                'user_info': user_info_serializer.data,
                'experience': experience_serializer.data,
                'template_content': template.html_content
            }
            
            # Generate PDF
            pdf_file = generate_pdf(context)
            
            # Return the PDF file
            return Response({'pdf_file': pdf_file}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    



class CreateResumeAPIView(APIView):
    def post(self, request):
        template_id = request.data.get('template_id')
        try:
            template = ResumeTemplate.objects.get(id=template_id)
        except ResumeTemplate.DoesNotExist:
            return Response({'error': 'Template not found'}, status=status.HTTP_404_NOT_FOUND)
        
        resume_data = create_resume_from_template(template)
        return Response(resume_data)


class GeneratePDFAPIView(APIView):
    def post(self, request):
        try:
            # Extract data from the request
            user_id = request.data.get('user_id')
            template_id = request.data.get('template_id')
            
            # Fetch user information based on the user ID
            user_info = PersonalInformation.objects.get(user_id=user_id)
            experience = Experience.objects.filter(user_id=user_id)
            
            # Fetch the selected template
            template = Template.objects.get(id=template_id)
            
            # Serialize user information and experience
            user_info_serializer = PersonalInformationSerializer(user_info)
            experience_serializer = ExperienceSerializer(experience, many=True)
            
            # Combine user information, experience, and template content
            context = {
                'user_info': user_info_serializer.data,
                'experience': experience_serializer.data,
                'template_content': template.html_content
            }
            
            # Generate PDF
            pdf_file = generate_pdf(context)
            
            # Return the PDF file
            return Response({'pdf_file': pdf_file}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

