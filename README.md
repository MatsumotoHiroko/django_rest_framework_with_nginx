# environment
Django
Python 3.6
Nginx
PostgreSQL 9.6

# recommend HTTP Clien
[HTTPie](https://httpie.org/)
# installation
## builds docker compose
```
$ docker-compose up -d 
```

## creates Superuser
```
$ docker-compose run web /code/manage.py createsuperuser --username admin --email admin@admin.example.com
>Starting myapp-api-test_db_1 ... done
>Password: # Input user password
>Password (again): 
>Superuser created successfully.
```

# execution
## get Token
```
$ http POST :8000/login username=admin password=(your password)
>HTTP/1.1 200 OK
>Allow: POST, OPTIONS
>Content-Length: 52
>Content-Type: application/json
>Date: Tue, 19 Feb 2019 09:38:58 GMT
>Server: WSGIServer/0.2 CPython/3.6.6
>Vary: Accept
>X-Frame-Options: SAMEORIGIN
>
>{
>    "token": "e0f8478728807148e4f6ad92173e8e87fd5d52c2"
>}
```

## create data
```
$ http POST :8000/books/ 'Authorization:Token e0f8478728807148e4f6ad92173e8e87fd5d52c2' name=Book1 price=200 published_at=2019-01-01T00:00:00Z
$ http POST :8000/books/1/rating/ 'Authorization:Token e0f8478728807148e4f6ad92173e8e87fd5d52c2' value=1 
```

## get data
### book list
```
$ http GET :8000/books/
```
### book detail
```
$ http GET :8000/books/1/
```

# testing
## executes unit test
```
$ docker-compose run web /code/manage.py test
>Starting myapp-api-test_db_1 ... done
>Creating test database for alias 'default'...
>System check identified no issues (0 silenced).
>.......
>----------------------------------------------------------------------
>Ran 7 tests in 0.218s
>
>OK
>Destroying test database for alias 'default'...
```