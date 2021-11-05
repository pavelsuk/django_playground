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
django-admin startproject mysite
```
