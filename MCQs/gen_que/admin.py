from django.contrib import admin
from .models import Question, Choice, TestSession, UserResponse


admin.site.register(Choice)
admin.site.register(Question)
admin.site.register(TestSession)
admin.site.register(UserResponse)
# admin.site.register(Choice)
# Register your models here.
