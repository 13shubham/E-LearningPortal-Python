import decimal
from django.contrib import admin
from .models import Topic, Course, Student, Order, Review

class CourseAdmin(admin.ModelAdmin):

    def price_discount(self, request, queryset):
        for course in queryset:
            course.price = course.price * decimal.Decimal('0.9')
            course.save()

    fields = [('title', 'topic'), ('price', 'num_reviews', 'for_everyone')]
    list_display = ('title', 'topic', 'price')
    price_discount.short_description = "Price has been reduced by 10%%"
    actions = ['price_discount']

class OrderAdmin(admin.ModelAdmin):
    fields = ('courses', ('student', 'order_status', 'order_date'))
    list_display = ('id', 'student', 'order_status', 'order_date', 'total_cost')

class CourseInline(admin.TabularInline):
    model = Course

class TopicAdmin(admin.ModelAdmin):
    fields = ['name', 'length']
    list_display = ['name', 'length']
    inlines = [CourseInline]

class StudentAdmin(admin.ModelAdmin):
    list_display =['first_name','last_name','level','courses_registered']

# Register your models here.
admin.site.register(Topic, TopicAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Review)
