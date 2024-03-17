from django.contrib import admin
# from .models import PersonalInformation, Education, ProfessionalExperience, Skill, Project, ResumeTemplate
from .models import ResumeTemplate, TemplateSelection

admin.site.register(ResumeTemplate)

admin.site.register(TemplateSelection)


# class PersonalInformationAdmin(admin.ModelAdmin):
#     list_display = ('user', 'first_name')
   

# admin.site.register(PersonalInformation, PersonalInformationAdmin)

# class EducationAdmin(admin.ModelAdmin):
#     list_display = ('user', 'degree', 'start_date', 'end_date')
 
#     search_fields = ('degree', 'user__username')

# admin.site.register(Education, EducationAdmin)

# class ProfessionalExperienceAdmin(admin.ModelAdmin):
#     list_display = ('user', 'start_date')
    

# admin.site.register(ProfessionalExperience, ProfessionalExperienceAdmin)

# class SkillAdmin(admin.ModelAdmin):
#     list_display = ('user', 'skill_name')
#     search_fields = ('skill_name', 'user__username')

# admin.site.register(Skill, SkillAdmin)

# class ProjectAdmin(admin.ModelAdmin):
#     list_display = ('user', 'project_name', 'start_date', 'end_date', 'url')
#     search_fields = ('project_name', 'user__username')

# admin.site.register(Project, ProjectAdmin)

# admin.site.register(ResumeTemplate)