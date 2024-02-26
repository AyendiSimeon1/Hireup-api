from django.db import models
from django.contrib.auth.models import User

class PersonalInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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

class ProfessionalExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    positiion_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    work_summary = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.job_title} at {self.company} in {self.user}"

class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    institution_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=255)
    field_study = models.CharField(max_length=20)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.degree} at {self.institution}"

class Skill(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skill_name = models.CharField(max_length=255)

    def __str__(self):
        return f"Username: {self.skill_name}, Email: {self.user}"

class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.project_name

class Socials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    twitter = models.CharField(max_length=20, blank=True)
    github = models.CharField(max_length=20, blank=True)
    linkedin = models.CharField(max_length=20, blank=True)

class ProfessionalSummary(models.Model):
    user = models.ForeignKey(User, on_delete=models)

class ResumeTemplate(models.Model):
    name = models.CharField(max_length=255)
    design = models.TextField() 

    def __str__(self):
        return self.name