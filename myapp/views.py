# Import necessary classes
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from .models import Topic, Course, Student, Order, Review
# from django.db.models.functions import Upper
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.http import HttpResponse
from .forms import SearchForm, OrderForm, ReviewForm, StudentForm, TopicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime


# Create your views here.
class IndexView(View):
    template_name = 'myapp/index.html'

    def get(self, request):
        last_login = None
        if request.session.get('last_login', False):
            last_login = datetime.strptime(request.session.get('last_login'), '%Y-%m-%d %H:%M:%S.%f')
            time_elapsed = datetime.now() - last_login
            if time_elapsed.seconds > 3600:
                logout(request)
            else:
                pass
        else:
            pass

        top_list = Topic.objects.all().order_by('id')[:10]
        return render(request, 'myapp/index.html', {'top_list': top_list, 'last_login': last_login})

def about(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    # Get the number of visits to the site.
    if 'about_visits' in request.COOKIES.keys():
        number_visits = request.COOKIES['about_visits']
    else:
        number_visits = 0
    if number_visits:
        number_visits = int(number_visits) + 1
    else:
        number_visits = 0
    response = render(request, 'myapp/about.html', {'top_list': top_list,
                                                        'number_visits': number_visits})
    response.set_cookie('about_visits', value=number_visits, max_age=300)
    return response;

class DetailView(View):
    template_name= 'myapp/detail.html'
    def get(self, request, topic_id):
        top_list = Topic.objects.all().order_by('id')[:10]
        # should display the name (in uppercase), length and the list of courses for that topic.
        topic_list = get_object_or_404(Topic, id=topic_id)
        # topic_upper = topic.annotate(name_upper=Upper('name'))
        # str(   topic_upper[0].name_upper)
        course_list = Course.objects.filter(topic=topic_id)
        course_length = course_list.__len__()
        return render(request, 'myapp/detail.html', {'course_list': course_list,
                                                     'topic_list': topic_list, 'top_list': top_list,
                                                     'course_length': course_length})

#def detail(request, topic_id):
    #top_list = Topic.objects.all().order_by('id')[:10]
    # should display the name (in uppercase), length and the list of courses for that topic.
    #topic_list = get_object_or_404(Topic, id=topic_id)
    # topic_upper = topic.annotate(name_upper=Upper('name'))
    # str(   topic_upper[0].name_upper)
    #course_list = Course.objects.filter(topic=topic_id)
    #course_length = course_list.__len__()
    #return render(request, 'myapp/detail.html', {'course_list': course_list,
        #                                                 'topic_list': topic_list, 'top_list': top_list,
#                                                'course_length': course_length})

def findcourses(request):
    top_list = Topic.objects.all().order_by('id')[:10]
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            length = form.cleaned_data['length']
            max_price = form.cleaned_data['max_price']
            courselist = []
            topics = Topic.objects.filter(length=length)
            for top in topics:
                courselist = courselist + list(top.courses.filter(price__lte=max_price))
            return render(request, 'myapp/results.html', {'courselist': courselist,
                                                              'top_list': top_list,
                                                              'name': name, 'length': length})
        else:
            return HttpResponse('Invalid data')
    else:
        form = SearchForm()
        return render(request, 'myapp/findcourses.html', {'form': form})


def place_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            courses = form.cleaned_data['courses']
            order = form.save(commit=True)
            student = order.student
            status = order.order_status
            order.save()
            if status == 1:
                for c in order.courses.all():
                    student.registered_courses.add(c)
            return render(request, 'myapp/order_response.html', {'courses': courses, 'order': order})
        else:
            return render(request, 'myapp/place_order.html', {'form': form})

    else:
        form = OrderForm()
        return render(request, 'myapp/place_order.html', {'form': form})

def review(request):
    if request.user.is_authenticated:
        try:
            user = Student.objects.get(username=request.user.username)
            if user.level == 'UG' or user.level == 'PG':
                if request.method == 'POST':
                    form = ReviewForm(request.POST)
                    if form.is_valid():
                        rating = form.cleaned_data['rating']
                        if (rating < 1 or rating > 5):
                            form.add_error('rating', 'You must enter a rating between 1 and 5')
                            return render(request, 'myapp/review.html', {'form': form})
                        review = form.save()
                        course_id = review.course.id
                        course = Course.objects.get(id=course_id)
                        course.num_reviews = course.num_reviews + 1
                        course.save()
                        response = redirect('myapp:index')
                        return response
                    else:
                        return render(request, 'myapp/review.html', {'form': form})
                else:
                    form = ReviewForm()
                    return render(request, 'myapp/review.html', {'form': form})
            else:
                return HttpResponse('Only undergraduate or postgraduate students can fill the review form.')
        except Student.DoesNotExist:
            return HttpResponse('You are not a registered student!')
    else:
        return HttpResponse('You must be logged in to provide reviews')


def review(request):
    if request.user.is_authenticated:
        try:
            user = Student.objects.get(username=request.user.username)
            if user.level == 'UG' or user.level == 'PG':
                if request.method == 'POST':
                    form = ReviewForm(request.POST)
                    if form.is_valid():
                        rating = form.cleaned_data['rating']
                        if (rating < 1 or rating > 5):
                            form.add_error('rating', 'You must enter a rating between 1 and 5')
                            return render(request, 'myapp/review.html', {'form': form})
                        review = form.save()
                        course_id = review.course.id
                        course = Course.objects.get(id=course_id)
                        course.num_reviews = course.num_reviews + 1
                        course.save()
                        response = redirect('myapp:index')
                        return response
                    else:
                        return render(request, 'myapp/review.html', {'form': form})
                else:
                    form = ReviewForm()
                    return render(request, 'myapp/review.html', {'form': form})
            else:
                return HttpResponse('Only undergraduate or postgraduate students can fill the review form.')
        except Student.DoesNotExist:
            return HttpResponse('You are not a registered student!')
    else:
        return HttpResponse('You must be logged in to provide reviews')

def user_login(request):
    request.session['last_login'] = str(datetime.now())
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('myapp:index'))
            else:
                return HttpResponse('Your account is disabled.')
        else:
            return HttpResponse('Invalid login details.')
    else:
        # user is already logged in so, redirect them to index
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('myapp:index'))
        # render the login form
        return render(request, 'myapp/login.html')

@login_required
def user_logout(request):
    logout(request)
    return render(request, 'myapp/logout.html')

# my account for student
def myaccount(request):
    username = request.user.username
    try:
        user = Student.objects.get(id=request.user.id)
    except Student.DoesNotExist:
        user = None
    if user:
        firstName = user.first_name
        lastName = user.last_name
        url = False
        if user.profile_image:
            url = user.profile_image.url
        return render(request, 'myapp/myaccount.html',
                      {'first_name': firstName, 'last_name': lastName, 'courses': user.registered_courses.all(),
                       'topics': user.interested_in.all(), 'url': url})
    else:
        courses = Course.objects.all().order_by('id')
        topics=Topic.objects.all().order_by('id')
        return render(request, 'myapp/login.html', {'courses': courses,'topic':topics})

def register_user(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            password = form.cleaned_data['password']
            student = form.save()
            student.set_password(password)
            student.save()
            response = redirect('myapp:login')
            return response
        else:
            return render(request, 'myapp/register.html', {'form': form})
    else:
        form = StudentForm()
        return render(request, 'myapp/register.html', {'form': form})


def myorders(request):
    if request.user.is_authenticated:
        try:
            user = Student.objects.get(id=request.user.id)
        except Student.DoesNotExist:
            user = None
        if user:
            orders = Order.objects.filter(student=user)
            return render(request, 'myapp/myorders.html', {'orders': orders, 'user': user})
        else:
            return HttpResponse('You are not a registered student!')
    else:
        return HttpResponse('You are not logged in. Please login to view orders')

# list of numbers
mylist = [5, -3, 0, 12, 7, 4]
i = 0

# using while loop
while (i < len(mylist)):

    # checking condition for zero
    if mylist[i] == 0:
        print("Zero")
        # checking condition for zero and even
    if mylist[i] != 0 and mylist[i] % 2 == 0:
        print("Even")
        # checking condition for zero and odd
    if mylist[i] != 0 and mylist[i] % 2 != 0:
        print("Odd")

        # increment i
    i += 1