from django.db import models
from django.contrib.auth.models import AbstractBaseUser, Group, Permission


class PersonalInformation(models.Model):
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    job_title = models.CharField(max_length=20, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.first_name


class Skill(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class ProfessionalExperience(models.Model):
    position_title = models.CharField(max_length=255, null=True, blank=True)
    company_name = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    work_summary = models.TextField(blank=True, null=True)

class Education(models.Model):
    institution_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_study = models.CharField(max_length=20)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.degree} at {self.institution_name}"


class Project(models.Model):
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.project_name


class Socials(models.Model):
    twitter = models.CharField(max_length=20, blank=True)
    github = models.CharField(max_length=20, blank=True)
    linkedin = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"Twitter: {self.twitter}, Github: {self.github}, Linkedin: {self.linkedin}"


class ProfessionalSummary(models.Model):
    content = models.TextField()

    def __str__(self):
        return self.content[:20] + "..."  

class ResumeTemplate(models.Model):
    name = models.CharField(max_length=255)  
    content = models.TextField()  
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

class TemplateSelection(models.Model):
    template_name = models.CharField(max_length=20)

    def __str__(self):
        return self.template_name


class User(AbstractBaseUser): 
    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Change this to a unique name
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # Change this to a unique name
        blank=True,
    )
    id = models.AutoField(primary_key=True) 
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    personal_info = models.OneToOneField(PersonalInformation, on_delete=models.CASCADE, related_name='user')
    skills = models.ManyToManyField(Skill, blank=True, related_name='skills')
    professional_experiences = models.ManyToManyField(ProfessionalExperience, blank=True, null=True)
    educations = models.ManyToManyField(Education,  related_name="educations")
    projects = models.ManyToManyField(Project, related_name="user_projects")
    socials = models.ForeignKey(Socials, on_delete=models.CASCADE,related_name="user_socials")
    professional_summary = models.ForeignKey(ProfessionalSummary, on_delete=models.CASCADE, related_name="user_summary")
    selected_template = models.ForeignKey(TemplateSelection, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" 


