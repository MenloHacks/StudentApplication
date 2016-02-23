from django.contrib import admin

from application.models import Application, Profile

from import_export.admin import ImportExportModelAdmin
from import_export import resources

from application.models import Application, Profile

# Register your models here.
class ApplicationResource(resources.ModelResource):
    class Meta:
        model = Application
        
class ProfileResource(resources.ModelResource):
    class Meta:
        model = Profile
        
        
class ApplicationAdmin(ImportExportModelAdmin):
    resource_class = ApplicationResource
    pass

class ProfileAdmin(ImportExportModelAdmin):
    resource_class = ProfileResource
    pass


admin.site.register(Application, ApplicationAdmin)
admin.site.register(Profile, ProfileAdmin)