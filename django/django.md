- ### for version cheack:
```
django-admin --version
```
### ---------- Working with Inner Project Directories ----------
- ### for creating project
```
django-admin startproject project_name
python manage.py runserver
```
### 1. Create views.py:
```commandline
# views.py

from django.http import HttpResponse

def home(request):
    return HttpResponse('THIS IS HOME PAGE')

```
### 2. Update urls.py:
```commandline
# urls.py

from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', views.contact),
]
```

### ---------- Working with Inner App Directories ----------
- ### for creating an application
```
django-admin startapp app_name
```
### 1. Update settings.py:
```
# settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app_name',
]
```

### 2. Create urls.py:
```commandline
from django .urls import path
from django.urls import path
from  . import views

urlpatterns = [
    path("courses/",views.courses),
    path("",views.home),
    path("about/",views.about),

]
```
### 3. Create views.py:
```commandline
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse("THIS IS FIRST_APP PAGE")
def courses(request):
    return HttpResponse("THIS IS FIRST_APP COURSES PAGE")
def about(request):
    return HttpResponse("THIS IS FIRST_APP ABOUT PAGE")
```

