<h1 style="text-align: center">Django REST API</h1>

<h2>Installation Steps:</h2>

<p>◾First, make a new virtual envirnoment, by running the follwing commands</p>

``` 
pipenv shell
 ```

<p>or</p>

```
python -m venv EnvirnomentName
```


<p>◾Install the dependencies by running the following commands:</p>
Using pipenv:

```
pipenv install
```
Using pip:
```
pip install -r requirements.txt
```

<p>◾Replace the field below with your MySQL Configurations</p>

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'storefront2',
        'HOST': 'localhost',
        'USER': 'root',
        'PASSWORD': 'ILoveDjango'
    }
}
```

<p>◾The API doesn't have any data you can add the data and try it yourself.</p>

<p>◾Create a superuser and generate an access token to access the endpoint using the commands below.</p>

To create a super user:
```
python manage.py make createsuperuser

```

<p>◾To Generate an access token go to /auth/jwt/create and enter your username and password to get a token.</p>


