# from django.contrib import admin
# from .models import Problem

# class ProblemAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'difficulty', 'is_public', 'created_at')
#     list_filter = ('difficulty', 'is_public', 'created_at')
#     search_fields = ('title', 'description')
#     readonly_fields = ('created_at', 'updated_at')
#     fieldsets = (
#         (None, {
#             'fields': ('title', 'description', 'author')
#         }),
#         ('Constraints', {
#             'fields': ('time_limit', 'memory_limit', 'difficulty')
#         }),
#         ('Visibility', {
#             'fields': ('is_public',)
#         }),
#         ('Dates', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         })
#     )

#     def save_model(self, request, obj, form, change):
#         if not obj.author_id:
#             obj.author = request.user
#         super().save_model(request, obj, form, change)

# admin.site.register(Problem, ProblemAdmin)
# from django.contrib import admin
# from .models import Problem, Submission


# admin.site.register(Submission)

# from django.contrib import admin
# from .models import Problem, Submission, 


# @admin.register(Problem)
# class ProblemAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'difficulty', 'is_public', 'created_at')
#     list_filter = ('difficulty', 'is_public', 'created_at')
#     search_fields = ('title', 'description')
#     readonly_fields = ('created_at', 'updated_at')
#     prepopulated_fields = {"slug": ("title",)}  # for auto slug generation

#     fieldsets = (
#         (None, {
#             'fields': ('title', 'slug', 'description', 'author')
#         }),
#         ('Constraints', {
#             'fields': ('time_limit', 'memory_limit', 'difficulty')
#         }),
#         ('I/O Format', {
#             'fields': ('input_description', 'output_description', 'sample_input', 'sample_output')
#         }),
#         ('Visibility', {
#             'fields': ('is_public',)
#         }),
#         ('Dates', {
#             'fields': ('created_at', 'updated_at'),
#             'classes': ('collapse',)
#         }),
#     )

#     def save_model(self, request, obj, form, change):
#         if not obj.author_id:
#             obj.author = request.user
#         super().save_model(request, obj, form, change)


# @admin.register(Submission)
# class SubmissionAdmin(admin.ModelAdmin):
#     list_display = ('user', 'problem', 'language', 'verdict', 'created_at')
#     list_filter = ('verdict', 'language', 'created_at')
#     search_fields = ('user__username', 'problem__title')


# admin.site.register(Problem, ProblemAdmin)
# from django.contrib import admin
# from .models import Problem, Submission


# admin.site.register(Submission)
from django.contrib import admin
from .models import Problem, Submission, TestCase

class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1  # number of empty forms shown by default
    fields = ('input_data', 'expected_output', 'is_sample')

class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'difficulty', 'is_public', 'created_at')
    list_filter = ('difficulty', 'is_public', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [TestCaseInline]  # 🔥 Add inline here

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'author')
        }),
        ('Constraints', {
            'fields': ('time_limit', 'memory_limit', 'difficulty')
        }),
        ('Input/Output Format', {
            'fields': ('input_description', 'output_description', 'sample_input', 'sample_output')
        }),
        ('Visibility', {
            'fields': ('is_public',)
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Problem, ProblemAdmin)
admin.site.register(Submission)
