from django.contrib import admin
from .models import Problem

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'difficulty', 'is_public', 'created_at')
    list_filter = ('difficulty', 'is_public', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'author')
        }),
        ('Constraints', {
            'fields': ('time_limit', 'memory_limit', 'difficulty')
        }),
        ('Visibility', {
            'fields': ('is_public',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Problem, ProblemAdmin)
from django.contrib import admin
from .models import Problem, Submission


admin.site.register(Submission)
