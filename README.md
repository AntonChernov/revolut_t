
## **Preperation:**

#### create environment: `python3.7 -m venv <venv_name>`

#### activate env `source <venv_name>/bin/activate`

#### install libs `pip install -r requirements.txt`


## **Django installation/preparation**

#### run command `./manage.py migrate`

#### run `./manage.py createsuperuser` enter username, password, email

#### go to `http://host:port/admin` enter credentials from your user and go to Token page

#### for API request you need put to headers next: 
`
"headers": {
    "Accept": "application/json",
    "Authorization": "Token <your tokken from previous step>",
    "Content-Type": "application/json;charset=utf-8"
  }
` 


**CLI Command**

#### `python nested.py --currency EUR,FBP`

#### run tests for cli  `python -m unittest tests_cli.py`

**API**

#### run `./manage.py runserver 127.0.0.1:8800`

#### do request on http://host:port/api/nested/?currency=EUR,USD   <-- example

#### run tests `./manage.py test revolut_test.tests`

## **What i add if i have more time**

#### Serializers for APIS (For some reason serializer after serialization de serialization return an empty OrderedDict)

#### SWAGGER documentation for API

#### More test, test poor

#### Dockerize the project maybe add cookiecutter for use the same template(if project build as Microservices) Not sure about Django good for Microservices