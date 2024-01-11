from django.db import models

# class PersonalInformation(models.Model):
#     first_name = models.CharField(max_length=50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField()
#     phone_number = models.CharField(max_length=20)
#     address = models.TextField()

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

# class Education(models.Model):
#     user = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)
#     degree = models.CharField(max_length=100)
#     institution = models.CharField(max_length=150)
#     graduation_year = models.PositiveIntegerField()

#     def __str__(self):
#         return f"{self.degree} from {self.institution}"

# class WorkExperience(models.Model):
#     user = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)
#     job_title = models.CharField(max_length=100)
#     company = models.CharField(max_length=150)
#     start_date = models.DateField()
#     end_date = models.DateField(null=True, blank=True)
#     description = models.TextField()

#     def __str__(self):
#         return f"{self.job_title} at {self.company}"

# class Skill(models.Model):
#     user = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)
#     skill_name = models.CharField(max_length=100)
#     proficiency_level = models.CharField(max_length=20)

#     def __str__(self):
#         return self.skill_name

# class Project(models.Model):
#     user = models.ForeignKey(PersonalInformation, on_delete=models.CASCADE)
#     project_name = models.CharField(max_length=150)
#     description = models.TextField()
#     start_date = models.DateField()
#     end_date = models.DateField(null=True, blank=True)
#     url = models.URLField(blank=True, null=True)

#     def __str__(self):
#         return self.project_name
