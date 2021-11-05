# Writing your first Django app

## Sources

- Tutorial on [Djangoproject](https://docs.djangoproject.com/en/3.2/intro/tutorial01/)
- Czechitas/Úvod do programování 2 - Python/Python pro web/[Instalace](https://kodim.cz/czechitas/progr2-python/python-pro-web/instalace)  

## Installation

- Install python & django - either by pip:

    ``` bash
    py -m pip install django
    ```

    or conda - in case you use conda virtual environments

    ``` bash
    conda install -c conda-forge django
    ```

- Test if `django` is installed

  ``` bash
  python -m django --version
  ```

## First Project

- Jumpstart the project by

``` bash
django-admin startproject <your_site>
```

- Create your first app **pools** within root folder

``` bash
cd <your_site>
python manage.py startapp polls
```

- Edit views.py

``` python
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
```

- Create/Edit **urls.py**

``` python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
]
```

- Edit urls.py in <my_site> folder

``` python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
```

- Run `python manage.py runserver`
- Check [http://localhost:8000/polls/](http://localhost:8000/polls/)

- Play with urls.py in pools directory to include other pathes
  
## Database setup

- we need to create the tables in the database before we can use them. To do that, run the following command:

``` bash
python manage.py migrate
```

## Creating models

- we’ll create two models: **Question** and **Choice**. A **Question** has a question and a publication date. A **Choice** has two fields: the text of the choice and a vote tally. Each Choice is associated with a Question.
- Edit pools/models.py
  
``` python
from django.db import models


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
```

We’ll cover them in more depth in a later part of the tutorial, but for now, remember the three-step guide to making model changes:

- Change your models (in models.py).
- Run `python manage.py makemigrations` to create migrations for those changes
- Run `python manage.py migrate` to apply those changes to the database.
