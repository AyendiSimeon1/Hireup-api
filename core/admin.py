from django.contrib import admin
from .models import PersonalInformation, Education, WorkExperience, Skill, Project


class PersonalInformationAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'email', 'phone_number')
    search_fields = ('full_name', 'email')

admin.site.register(PersonalInformation, PersonalInformationAdmin)

class EducationAdmin(admin.ModelAdmin):
    list_display = ('user', 'degree', 'institution', 'start_date', 'end_date')
    list_filter = ('institution', 'degree')
    search_fields = ('degree', 'institution', 'user__username')

admin.site.register(Education, EducationAdmin)

class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'job_title', 'company', 'start_date', 'end_date')
    list_filter = ('company', 'job_title')
    search_fields = ('job_title', 'company', 'user__username')

admin.site.register(WorkExperience, WorkExperienceAdmin)

class SkillAdmin(admin.ModelAdmin):
    list_display = ('user', 'skill_name')
    search_fields = ('skill_name', 'user__username')

admin.site.register(Skill, SkillAdmin)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('user', 'project_name', 'start_date', 'end_date', 'url')
    search_fields = ('project_name', 'user__username')

admin.site.register(Project, ProjectAdmin)

