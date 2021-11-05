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

## Playing with the API

``` python
python manage.py shell
```

- see the [tutorial](https://docs.djangoproject.com/en/3.2/intro/tutorial02/)
- For more information on model relations, see [Accessing related objects](https://docs.djangoproject.com/en/3.2/ref/models/relations/). For more on how to use double underscores to perform field lookups via the API, see [Field lookups](https://docs.djangoproject.com/en/3.2/topics/db/queries/#field-lookups-intro). For full details on the database API, see our [Database API reference](https://docs.djangoproject.com/en/3.2/topics/db/queries/).

## Introducing the Django Admin

### Philosophy

Generating admin sites for your staff or clients to add, change, and delete content is tedious work that doesn’t require much creativity. For that reason, Django entirely automates creation of admin interfaces for models.

Django was written in a newsroom environment, with a very clear separation between “content publishers” and the “public” site. Site managers use the system to add news stories, events, sports scores, etc., and that content is displayed on the public site. Django solves the problem of creating a unified interface for site administrators to edit content.

The admin isn’t intended to be used by site visitors. It’s for site managers.

### Creating an admin user

``` bash
python manage.py createsuperuser
```

- start the server

``` bash
python manage.py runserver
```

- visit [http://localhost:8000/admin](http://localhost:8000/admin)
- we need to tell the admin that Question objects have an admin interface. To do this, open the [polls2/admin.py](pasusite/polls2/admin.py) file, and edit it to look like this:

``` python
from django.contrib import admin
from .models import Question
admin.site.register(Question)
```

- and play with [the admin interface](http://localhost:8000/admin) again

## Writing more views ([Tutorial 3](https://docs.djangoproject.com/en/3.2/intro/tutorial03/))

- add a few more views to polls/views.py

``` python
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
```

- Wire these new views into the polls.urls module by adding the following path() calls

``` python
from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('vote/<int:question_id>/', views.vote, name='vote'),
]]
```

- and try it
    - [http://localhost:8000/polls/1](http://localhost:8000/polls/1)
    - [http://localhost:8000/polls/13/result/](http://localhost:8000/polls/13/result/)
    - [http://localhost:8000/polls/2/vote/](http://localhost:8000/polls/2/vote/)
    - [http://localhost:8000/polls/vote/2](http://localhost:8000/polls/vote/2)
  
## Write views that actually do something

### Let's hardcode it first (ugly, but working)

- [polls2/views.py](polls2/../pasusite/polls2/views.py)

``` python
from django.http import HttpResponse

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

# Leave the rest of the views (detail, results, vote) unchanged
```

### Let's start using templates, instead of hardcoded html

- create a directory called **templates** in your **polls** directory. Django will look for templates in there
- Within the templates directory you have just created, create another directory called polls, and within that create a file called index.html. In other words, your template should be at polls/templates/polls/index.html. Because of how the app_directories template loader works as described above, you can refer to this template within Django as polls/index.html.

- Add code in polls/templates/polls/index.html

``` javascript
{% if latest_question_list %}
    <ul>
    {% for question in latest_question_list %}
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
    {% endfor %}
    </ul>
{% else %}
    <p>No polls are available.</p>
{% endif %}
```

- update our index view in polls/views.py to use the template

``` python
from django.http import HttpResponse
from django.template import loader

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))

```

### A shortcut: render()

It’s a very common idiom to load a template, fill a context and return an HttpResponse object with the result of the rendered template. Django provides a shortcut. Here’s the full index() view (polls/views.py), rewritten:

``` python
from django.shortcuts import render

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
```

## Let's show details of the question

- Add in polls/view/py

``` python
from django.http import Http404
from django.shortcuts import render

from .models import Question
# ...
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
```

- and add polls/detail.html

``` javascript
{{ question }}
```

- let's add 404 handling by A **shortcut: `get_object_or_404()`** 

``` python
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
```
