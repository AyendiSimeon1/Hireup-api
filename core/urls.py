from django.urls import path, include
from .views import RegisterView, LoginView, Profile, ResumeTemplateList
from rest_framework.routers import DefaultRouter
from .views import (
    PersonalInformationViewSet,
    EducationViewSet,
    WorkExperienceViewSet,
    SkillViewSet,
    ProjectViewSet,
)

router = DefaultRouter()
router.register(r'personal-information', PersonalInformationViewSet)
router.register(r'education', EducationViewSet)
router.register(r'work-experience', WorkExperienceViewSet)
router.register(r'skill', SkillViewSet)
router.register(r'project', ProjectViewSet)


urlpatterns= [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', Profile.as_view(), name='profile'),
    path('resume-templates/', ResumeTemplateList, name='resume-templates'),
    path('', include(router.urls)),

]