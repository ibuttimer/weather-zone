# Weather-Zone

Weather-Zone is a weather forecast application utilising third-party weather forecast data.

## Development and Local Deployment
### Environment
The development environment requires:

| Artifact                                 | Download and installation instructions       |
|------------------------------------------|----------------------------------------------|
| [Node.js](https://nodejs.org/)           | https://nodejs.org/en/download/              |
| [npm](https://www.npmjs.com/)            | Included with Node.js installation           |
| [git](https://git-scm.com/)              | https://git-scm.com/downloads                |
| [Python](https://www.python.org/)        | https://www.python.org/downloads/            |
| [Poetry](https://python-poetry.org/)     | https://python-poetry.org/docs/#installation |
| [Django](https://www.djangoproject.com/) | https://www.djangoproject.com/download/      |

### Setup
#### Clone Repository
In an appropriate folder, run the following commands:
```shell
> git clone https://github.com/ibuttimer/weather-zone.git
> cd weather-zone
```
Alternatively, most IDEs provide an option to create a project from Version Control.

#### Virtual Environment
It is recommended that a virtual environment be used for development purposes.
There are numerous options available; e.g. [venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment), [pyenv](https://github.com/pyenv/pyenv) etc. 

Please see [Switching between environments](https://python-poetry.org/docs/managing-environments/#switching-between-environments).

#### Environment Setup
In a terminal window, in the `weather-zone` folder, run the following command to setup required environment artifacts:
```shell
> npm install
```

#### Python Setup
In the `weather-zone` folder, run the following command to install the necessary python packages:
```shell
> poetry install
```

###### Table 1: Configuration settings
| Key                      | Value                                                                                                                                                                              |
|--------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ENV_FILE                 | If using an environment file, specifies the file to use. Defaults to `.env` in the project root folder.                                                                            |
| PORT                     | Port application is served on; default 8000                                                                                                                                        |
| DEBUG                    | A boolean that turns on/off debug mode; see [Boolean environment variables](#boolean-environment-variables)                                                                        |
| SECRET_KEY               | [Secret key](https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-SECRET_KEY) for a particular Django installation. See [Secret Key Generation](#secret-key-generation) |
| DATABASE_URL             | [Database url](https://docs.djangoproject.com/en/4.2/ref/settings/#databases)                                                                                                      |
| FONTAWESOME_URL          | Fontawesome kit url. See [Use a Kit](https://fontawesome.com/docs/web/setup/use-kit)                                                                                               |
| REQUESTS_TIMEOUT         | Requests timeout in seconds                                                                                                                                                        |

# TODO add STORAGE_PROVIDER environment variables

#### Boolean environment variables
Set environment variables evaluating a boolean value, should be set to any of `true`, `on`, `ok`, `y`, `yes` or `1` to set true, otherwise the variable is evaluated as false.

#### Environment variables
Set environment variables corresponding to the keys in [Table 1: Configuration settings](#table-1-configuration-settings).

##### Secret Key Generation
A convenient method of generating a secret key is to run the following command and copy its output.

```shell
$ python -c "import secrets; print(secrets.token_urlsafe())"
```

### Before first run
Before running the application for the first time following cloning from the repository and setting up a new database,
the following steps must be performed, from a terminal window, in the `weather-zone` folder.

#### Initialise the database
````shell
$ python manage.py migrate
````
#### Create a superuser
Enter `Username`, `Password` and optionally `Email address`.
````shell
$ python manage.py createsuperuser
````

#### Build Bootstrap
Build the customised version of Bootstrap.
````shell
$ npm run build
````

### Run server
In order to run the development server, run the following command from the `weather-zone` folder:

````shell
$ python manage.py runserver
````

By default, the server runs on port 8000 on the IP address 127.0.0.1.
See [runserver](https://docs.djangoproject.com/en/4.1/ref/django-admin/#runserver) for details on passing an IP address and port number explicitly.

### Application structure
The application structure is as follows:

```
├─ README.md            - this file
├─ docs                 - documentation
├─ data                 - application data
├─ locale               - translation files
├─ manage.py            - application entry point
├─ weather_zone         - main Django application
├─ base                 - base Django application
├─ forecast             - application generating forecast data from provider data  
├─ met_eireann          - Met Éireann forecast provider application
└─ templates            - application templates
```

## Credits

The following resources were used to build the website.

### Content
- Logo [Weather forecast](https://icons8.com/icon/kLj4x6XyooyO/weather-forecast), [Universal Multimedia License Agreement for Icons8](https://icons8.com/license), by [Icons8](https://icons8.com).

    **Disclaimer:** The extraction and reuse of icons8 graphics is prohibited, as stated in the [license](https://icons8.com/license).
- The favicon for the site was generated by [RealFaviconGenerator](https://realfavicongenerator.net/) from [Weather forecast](https://icons8.com/icon/kLj4x6XyooyO/weather-forecast), [Universal Multimedia License Agreement for Icons8](https://icons8.com/license), by [Icons8](https://icons8.com)
- Weather forecast icons courtesy of [The Norwegian Broadcasting Corporation](https://nrkno.github.io/yr-weather-symbols/)
- [Wind direction icons](static/img/wind_icons) derived from [South icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/south)

### Code

- [Secret Key Generation](#secret-key-generation) courtesy of [Humberto Rocha](https://humberto.io/blog/tldr-generate-django-secret-key/)
 
