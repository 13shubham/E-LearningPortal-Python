from django import forms
from myapp.models import Order, Review, Student, Course, Topic

class SearchForm(forms.Form):
    LENGTH_CHOICES = [
        (8, '8 Weeks'),
        (10, '10 Weeks'),
        (12, '12 Weeks'),
        (14, '14 Weeks'),
    ]
    name = forms.CharField(max_length=100, required=False,label='Student Name')
    length = forms.TypedChoiceField(required=False, label='Preferred course duration', widget=forms.RadioSelect,
                           choices = LENGTH_CHOICES)
    max_price = forms.FloatField(required=True, min_value=0, label="Maximum price")

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['courses', 'student', 'order_status']
        widgets = {'courses': forms.CheckboxSelectMultiple(), 'order_type': forms.RadioSelect}
        labels = {'student': u'Student Name', }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer', 'course', 'rating', 'comments']
        widgets = {'course': forms.RadioSelect()}
        labels = {'reviewer': u'Please enter a valid email', 'rating' : u'An integer between 1 (worst) and 5 (best)' }

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'username', 'password', 'level', 'address', 'province',
                  'registered_courses','interested_in']
        widgets = {'registered_courses': forms.CheckboxSelectMultiple(), 'interested_in': forms.CheckboxSelectMultiple(), 'password': forms.PasswordInput}
        labels={'registered_courses': u'Register Courses'}

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'topic', 'price', 'for_everyone','description']

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'length']