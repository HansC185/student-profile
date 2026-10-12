from django.contrib import admin
from .models import Profile, Skill, Project, Photo


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'course', 'school')


admin.site.register(Skill)
admin.site.register(Project)
admin.site.register(Photo)
