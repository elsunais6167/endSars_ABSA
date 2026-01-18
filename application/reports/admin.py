from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Incidence)
admin.site.register(KnowledgeCategory)
admin.site.register(KnowledgeComment)
admin.site.register(ExpertKnowledge)