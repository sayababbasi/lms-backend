# # # apps/library/admin.py
# # # Developed by SAYAB

# # from django.contrib import admin
# # from .models import Book, Issue, Return

# # @admin.register(Book)
# # class BookAdmin(admin.ModelAdmin):
# #     list_display = ("title", "author", "available_copies")
# #     search_fields = ("title", "author")

# # @admin.register(Issue)
# # class IssueAdmin(admin.ModelAdmin):
# #     list_display = ("book", "student", "issued_at", "due_date")
# #     list_filter = ("due_date",)

# # @admin.register(Return)
# # class ReturnAdmin(admin.ModelAdmin):
# #     list_display = ("issue", "returned_at", "status")
# #     list_filter = ("status",)


# # backend/apps/library/admin.py
# # Developed by SAYAB

# from django.contrib import admin
# from .models import Book, Issue, Return

# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'isbn', 'copies_available')


# @admin.register(Issue)
# class IssueAdmin(admin.ModelAdmin):
#     list_display = ('book', 'issued_to', 'issue_date', 'due_date', 'returned')


# @admin.register(Return)
# class ReturnAdmin(admin.ModelAdmin):
#     list_display = ('issue', 'return_date', 'fine')

# File: backend/apps/library/admin.py
# Admin registration for library (Developed by SAYAB)

from django.contrib import admin
from .models import Book, BookIssue

admin.site.register(Book)
admin.site.register(BookIssue)
