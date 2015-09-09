from django.contrib import admin
from legion.models import Person, Company, Job, Industry, User, Lead, Snapshot, Document


admin.site.register(Industry)
admin.site.register(Lead)

admin.site.register(Document)
admin.site.register(User)

admin.site.register(Snapshot)

class CompanyAdmin(admin.ModelAdmin):
    search_fields = ('name',)
admin.site.register(Company, CompanyAdmin)



class JobAdmin(admin.ModelAdmin):
    search_fields = ('title',)
admin.site.register(Job, JobAdmin)


class PersonAdmin(admin.ModelAdmin):
    search_fields = ('name',)
admin.site.register(Person, PersonAdmin)

# Register your models here.
