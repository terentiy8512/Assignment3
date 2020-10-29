# Movie web application

## Description

This is a web application for assignment 3. In this web application I used different python libraries such as Flask framework, Jinja templating library and WTForms. The application also uses Flask Blueprints to maintain separation of concerns between application functions. Testing includes unit and end-to-end testing using the pytest tool.

## Installation

**Installation via requirements.txt**

```shell
$ cd Assignment3
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

When using PyCharm, set the virtual environment using 'File'->'Settings' and select 'Project:Assignment2' from the left menu. Select 'Project Interpreter', click on the gearwheel button and select 'Add'. Click the 'Existing environment' radio button to select the virtual environment. 

## Execution

**Running the application**

From the *Assignment2* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 


## Configuration

The *Assignment3/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.


## Testing

Testing requires that file *Assignment2/tests/conftest.py* be edited to set the value of `TEST_DATA_PATH`. You should set this to the absolute path of the *Assignment3/tests/data* directory. 

E.g. 

`TEST_DATA_PATH = os.path.join('A:',os.sep,'PythonProjects', 'Assignment 3', 'tests', 'data')`

assigns TEST_DATA_PATH with the following value (the use of os.path.join and os.sep ensures use of the correct platform path separator):

`C:\PythonProjects\Assignment3\tests\data`

You can then run tests from within PyCharm.

*Run tests by typing in terminal*: 
python -m pytest
 
