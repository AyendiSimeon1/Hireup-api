from django.urls import path, include
from .views import RegisterView, LoginView, Profile
from rest_framework.routers import DefaultRouter
from .views import (
    PersonalInformationViewSet,
    EducationViewSet,
    ProfessionalExperienceViewSet,
    SkillViewSet,
    ProjectViewSet,
    get_resume_template,
    ResumeTemplateList
)

router = DefaultRouter()
router.register(r'personal-information', PersonalInformationViewSet)
router.register(r'education', EducationViewSet)
router.register(r'Professional-experience', ProfessionalExperienceViewSet)
router.register(r'skill', SkillViewSet)
router.register(r'project', ProjectViewSet)


urlpatterns= [
    #path('resume-templates/', ResumeTemplateList.as_view(), name='resume-templates'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', Profile.as_view(), name='profile'),
    path('choose-resume-template/', get_resume_template.as_view(), name='get_resume_template'),
    path('resume-templates/', ResumeTemplateList.as_view(), name='resume-template'),
    path('', include(router.urls)),

]