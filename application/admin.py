from django.contrib import admin

from application.models import Application, Profile, ApplicationReview

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

class ApplicationReviewResource(resources.ModelResource):
    class Meta:
        model = ApplicationReview
        
        
class ApplicationAdmin(ImportExportModelAdmin):
    resource_class = ApplicationResource
    pass

class ProfileAdmin(ImportExportModelAdmin):
    resource_class = ProfileResource
    pass

class ApplicationReviewAdmin(ImportExportModelAdmin):
    resource_class = ApplicationReviewResource
    pass


admin.site.register(Application, ApplicationAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(ApplicationReview, ApplicationReviewAdmin)