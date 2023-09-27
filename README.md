# Weather-Zone

Weather-Zone is a weather forecast application utilising multiple third-party weather forecasters, to provide address-based weather forecasts.

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
There are numerous options available; e.g. [poetry](https://python-poetry.org/), [venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment), [pyenv](https://github.com/pyenv/pyenv) etc. 

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
| Key                                    | Value                                                                                                                                                                                                                                                                   |
|----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ENV_FILE                               | If using an environment file, specifies the file to use. Defaults to `.env` in the project root folder.                                                                                                                                                                 |
| PORT                                   | Port application is served on; default 8000                                                                                                                                                                                                                             |
| DEBUG                                  | A boolean that turns on/off debug mode; see [Boolean environment variables](#boolean-environment-variables)                                                                                                                                                             |
| SECRET_KEY                             | [Secret key](https://docs.djangoproject.com/en/4.2/ref/settings/#std-setting-SECRET_KEY) for a particular Django installation. See [Secret Key Generation](#secret-key-generation)                                                                                      |
| DATABASE_URL                           | [Database url](https://docs.djangoproject.com/en/4.2/ref/settings/#databases)                                                                                                                                                                                           |
| REMOTE_DATABASE_URL                    | Url of remote PostgreSQL database resource.<br>__Note:__ Only required for admin purposes, see database configuration under [Cloud-based Deployment](#cloud-based-deployment)                                                                                           |
| FONTAWESOME_URL                        | Fontawesome kit url. See [Use a Kit](https://fontawesome.com/docs/web/setup/use-kit)                                                                                                                                                                                    |
| REQUESTS_TIMEOUT                       | Requests timeout in seconds                                                                                                                                                                                                                                             |
| FORECAST_PROVIDERS                     | List of forecast providers to use, see [FORECAST_PROVIDERS environment variable](#forecast_providers-environment-variable).                                                                                                                                             |
| LOCATIONFORECAST_*&lt;provider id&gt;* | Individual forecast provider configuration settings, see [LOCATIONFORECAST_*&lt;provider id&gt;* environment variables](#locationforecast_provider-id-environment-variables).                                                                                           |
| DEFAULT_SEND_EMAIL                     | Email address to send emails from. Only valid when development mode is enabled, in production mode emails are sent from `EMAIL_HOST_USER`                                                                                                                               |
| EMAIL_HOST                             | SMTP server to send email. Only valid when production mode is enabled.                                                                                                                                                                                                  |
| EMAIL_USE_TLS                          | Use Transport Layer Security (TLS) flag; see [Boolean environment variables](#boolean-environment-variables), default true. Only valid when production mode is enabled.                                                                                                 |
| EMAIL_PORT                             | SMTP server port. Only valid when production mode is enabled.                                                                                                                                                                                                           |
| EMAIL_HOST_USER                        | Email user account to send email. Only valid when production mode is enabled.                                                                                                                                                                                           |
| EMAIL_HOST_PASSWORD                    | Email user account password. Only valid when production mode is enabled.                                                                                                                                                                                                |
| STORAGE_PROVIDER                       | Storage provider; set to `s3` to use an Amazon Web Service S3 bucket for storage or `default` to use Django's default storage                                                                                                                                           |
| EXTERNAL_HOSTNAME                      | [Hostname](https://docs.djangoproject.com/en/4.1/ref/settings/#allowed-hosts) of application on hosting service.<br>__Note:__ To specify multiple hosts, use a comma-separated list with no spaces.<br>__Note:__ Set to `localhost,127.0.0.1` in local development mode |
|                                        | **Amazon S3-specific**                                                                                                                                                                                                                                                  |
| AWS_ACCESS_KEY_ID                      | The access key for your AWS account.                                                                                                                                                                                                                                    |
| AWS_SECRET_ACCESS_KEY                  | The secret key for your AWS account.                                                                                                                                                                                                                                    |
| AWS_STORAGE_BUCKET_NAME                | AWS S3 bucket name.                                                                                                                                                                                                                                                     |
|                                        | **Development-specific configuration**                                                                                                                                                                                                                                  |
| CACHED_GEOCODE_RESULT                  | Cached Google Geocoding response to use; e.g. '[{"address_components": [{"long_name": "50", ... }]'                                                                                                                                                                     |
| CACHED_MET_EIREANN_RESULT              | Path relative to project root of forecast response to use; e.g. 'dev/data/met_eireann/cached_resp.xml'                                                                                                                                                                  |


#### Boolean environment variables
Set environment variables evaluating a boolean value, should be set to any of `true`, `on`, `ok`, `y`, `yes` or `1` to set true, otherwise the variable is evaluated as false.

#### FORECAST_PROVIDERS environment variable
The `locationforecast` application may be configured with multiple providers which utilise the
[Locationforecast](https://api.met.no/weatherapi/locationforecast/2.0/documentation) weather forecast API developed by Met Norway.

The `FORECAST_PROVIDERS` environment variable is a comma-separated list of providers to use, of the form `<provider app name>_<provider id>`.

The convention is to name the provider class in the form `<provider id>Provider` where `<provider id>` is camel-cased, e.g. `met_eireann` becomes `MetEireannProvider`.
And the module name should be `<provider id>.py` e.g. `met_eireann.py`.

E.g. the following configures two providers; `met_eireann` and `met_norway_classic`, which will load the `MetEireannProvider` and `MetNorwayClassicProvider` classes respectively.
````shell
FORECAST_PROVIDERS=locationforecast_met_eireann,locationforecast_met_norway_classic
````

See [Locationforecast](docs/readme.md#locationforecast) for more details on the providers.


#### LOCATIONFORECAST_*&lt;provider id&gt;* environment variables
The configuration for each provider in the [FORECAST_PROVIDERS environment variable](#forecast_providers-environment-variable) 
must be provided by an environment variable of the following format:

- Environment variable name

    LOCATIONFORECAST_*&lt;provider id&gt;*; where `<provider id>` is the id of the provider, e.g. `met_eireann`.
  
- Environment variable value

    A semicolon-seperated list of key-value pairs as outlined in the following table.

| Key       | Description                                                                                                                               |
|-----------|-------------------------------------------------------------------------------------------------------------------------------------------|
| name      | Display name of provider                                                                                                                  |
| url       | Provider website url.                                                                                                                     |
| data_url  | API url. See [Using unsafe characters in URLs](https://django-environ.readthedocs.io/en/latest/tips.html#using-unsafe-characters-in-urls) |
| latitude  | Latitude query parameter name, e.g. `latitude=lat`                                                                                        |
| longitude | Longitude query parameter name, e.g. `longitude=long`                                                                                     |
| from      | From date/time query parameter name                                                                                                       |
| to        | To date/time query parameter name                                                                                                         |
| tz        | A valid [IANA](https://www.iana.org/time-zones) timezone; e.g. `tz=Europe/Dublin`                                                         |
| country   | ISO 3166-1 alpha-2 country code for which provider provides forecasts; e.g. `country=IE`                                                  |

E.g. the following configure the `met_eireann` provider;
````shell
LOCATIONFORECAST_MET_EIREANN="name=Met Éireann;url=http://metwdb-openaccess.ichec.ie/metno-wdb2ts/locationforecast;latitude=lat;longitude=long;from=from;to=to;tz=UTC;country=IE"
````
**Note:** Keys not required by a particular provider should be omitted.

> See [Met Éireann Timezone anomaly](docs/readme.md#met-éireann-timezone-anomaly) for more details on the `tz` setting.

#### Environment variables
Set environment variables corresponding to the keys in [Table 1: Configuration settings](#table-1-configuration-settings).

##### Secret Key Generation
A convenient method of generating a secret key is to run the following command and copy its output.

```shell
$ python -c "import secrets; print(secrets.token_urlsafe())"
```

#### Email
Procedures differ depending on the email provider used.
for example, in order to configure Gmail as the email provider, the following actions must be performed.

* Login to [Gmail](https://mail.google.com/)
* Goto the Google Account settings and select [Security](https://myaccount.google.com/security)
* Under `How you sign in to Google` ensure 2-Step Verification is enabled
* Search for `App passwords` and create a new app password
* Copy the generated app password, and store securely


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

#### Configure authentication
From [django-allauth Post-Installation](https://django-allauth.readthedocs.io/en/latest/installation.html#post-installation)
- Add a Site for your domain in the database
  - Login to `http://&lt;domain&gt;/admin/sites/site/` as the previously created superuser, e.g. http://127.0.0.1:8000/admin/sites/site/
  - Add a Site for your domain (django.contrib.sites app).

    E.g.

    | Domain name    | Display name   |
    |----------------|----------------| 
    | 127.0.0.1:8000 | my domain      | 

    __Note:__ The id (primary key) of the site must be added to the application configuration. See `SITE_ID` in [Table 1: Configuration settings](#table-1-configuration-settings).

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
├─ addresses            - address application
├─ base                 - base application
├─ broker               - service broker application
├─ forecast             - application generating forecast data from provider data  
├─ locationforecast     - Locationforecast provider application
├─ user                 - user application
├─ utils                - utility functions
├─ weather_warning      - weather warning application
├─ static               - static files
└─ templates            - application templates
```

### Cloud-based Deployment
#### Render

The site was deployed on [Render](https://www.render.com).

##### Deployment
The following steps were followed to deploy the website:
- Login to Render in a browser
- From the dashboard select `New -> Web Service`
- Connect to the git repository
- Set following
  - `Name`, (e.g. `weather-zone`)
  - Choose an appropriate region
  - Select the git branch to deploy
  - Select `Python 3` runtime,
  - Set the Build command to `./build.sh`
  - Set the Start command to `gunicorn weather-zone.wsgi:application`
  - Select `Create Web Service`
- To provision the application with a database, such as an [ElephantSQL](https://www.elephantsql.com/) database.
  - For an [ElephantSQL](https://www.elephantsql.com/) database, follow the `Create a new instance` instructions under the `Getting started` section of the [ElephantSQL documentation](https://www.elephantsql.com/docs/index.html).
- Create an Amazon S3 bucket using [Storing Django Static and Media Files on Amazon S3](https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/).
  See [Configuring cross-origin resource sharing (CORS)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/enabling-cors-examples.html) and [CORS configuration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ManageCorsUsing.html)
  regarding setting the CORS configuration for the S3 bucket.
- Under `Environment -> Environment Variables` add the following environment variables

  | Key                     | Value                                                                                                                                                                                                                                                                                                          |
  |-------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
  | PYTHON_VERSION          | [Python version](https://render.com/docs/python-version)<br>**Note:** At time of writing the [Render Python3 environment](https://render.com/docs/native-environments) does not include the necessary Python headers to compile the `psycopg2` library for Python version 3.10.10, use *Python version 3.9.16* |
  | POETRY_VERSION          | [Poetry version](https://render.com/docs/python-version) |

  - Under `Environment -> Secret Files` add a file with the name `.env` with the same environment variables as specified in [Table 1: Configuration settings](#table-1-configuration-settings) with the following differences:
    - The following variables are *NOT* required
      - **Development-specific configuration**
    - Add the following variables:
      - **DATABASE_URL**
    - Add Amazon S3-specific settings

See [Table 1: Configuration settings](#table-1-configuration-settings) for details.

If any other settings vary from the defaults outlined in [Table 1: Configuration settings](#table-1-configuration-settings) they must be added as well.

- Select the `Manual Deploy` to deploy the application.

- Initialise the database and Create a superuser

  Involves the same procedure as outlined in [Initialise the database](#initialise-the-database) and [Create a superuser](#create-a-superuser)
  but may be run from the local machine.
  - From a [Development and Local Deployment](#development-and-local-deployment)
    - Initialise the database
      ````shell
      $ python manage.py migrate --database=remote
      ````
    - Create a superuser

      Enter `Username`, `Password` and optionally `Email address`.
      ````shell
      $ python manage.py createsuperuser --database=remote
      ````

    __Note:__ Ensure to specify the `--database=remote` option to apply the change to the database specified by the `REMOTE_DATABASE_URL` environment variable.

- Configure authentication

  Follow the same procedure as outlined in [Configure authentication](#configure-authentication) using the
  Heroku domain as `<domain>`, e.g. `weather-zone.onrender.com`

The live website is available at [https://weather-zone.onrender.com](https://weather-zone.onrender.com)

## Credits

The following resources were used to build the website.

### Content
- Logo [Weather forecast](https://icons8.com/icon/kLj4x6XyooyO/weather-forecast), [Universal Multimedia License Agreement for Icons8](https://icons8.com/license), by [Icons8](https://icons8.com).

    **Disclaimer:** The extraction and reuse of icons8 graphics is prohibited, as stated in the [license](https://icons8.com/license).
- The favicon for the site was generated by [RealFaviconGenerator](https://realfavicongenerator.net/) from [Weather forecast](https://icons8.com/icon/kLj4x6XyooyO/weather-forecast), [Universal Multimedia License Agreement for Icons8](https://icons8.com/license), by [Icons8](https://icons8.com)
- Weather forecast icons courtesy of [The Norwegian Broadcasting Corporation](https://nrkno.github.io/yr-weather-symbols/)
- [Wind direction icons](static/img/wind_icons) derived from [South icons created by Freepik - Flaticon](https://www.flaticon.com/free-icons/south)
- [Warning icon](https://icons8.com/icon/KarJz0n4bZSj/general-warning-sign), [Universal Multimedia License Agreement for Icons8](https://icons8.com/license), by [Icons8](https://icons8.com), background colour changed.
- [Boat icon](https://icons8.com/icon/66056/sail-boat), [Universal Multimedia License Agreement for Icons8](https://icons8.com/license), by [Icons8](https://icons8.com), background colour changed.
- [A icon](https://icons8.com/icon/38670/a), [Universal Multimedia License Agreement for Icons8](https://icons8.com/license), by [Icons8](https://icons8.com), background colour changed.
- [Breeze icon](https://icons8.com/icon/DSEt3IYZwWNb/breeze), [Universal Multimedia License Agreement for Icons8](https://icons8.com/license), by [Icons8](https://icons8.com), modified via Icons8 web tools.
- [Breeze icon](https://icons8.com/icon/i90FKzAM6LYA/breeze), [Universal Multimedia License Agreement for Icons8](https://icons8.com/license), by [Icons8](https://icons8.com), modified via Icons8 web tools.
- [Wind icon](https://icons8.com/icon/74197/wind), [Universal Multimedia License Agreement for Icons8](https://icons8.com/license), by [Icons8](https://icons8.com), modified via Icons8 web tools.
- [Storm icon](https://icons8.com/icon/EKkPq7Olo1Hp/storm), [Universal Multimedia License Agreement for Icons8](https://icons8.com/license), by [Icons8](https://icons8.com), modified via Icons8 web tools.
- [Tornado icon](https://icons8.com/icon/9309/tornado), [Universal Multimedia License Agreement for Icons8](https://icons8.com/license), by [Icons8](https://icons8.com), modified via Icons8 web tools.
- [Nothing Found icon](https://icons8.com/icon/83786/nothing-found), [Universal Multimedia License Agreement for Icons8](https://icons8.com/license), by [Icons8](https://icons8.com).
- [404 error icon](static/img/no-results.png) created by [Freepik - Flaticon](https://www.flaticon.com/free-icons/404-error)
- [Explosion icon](static/img/nuclear-explosion.png) created by [Freepik - Flaticon](https://www.flaticon.com/free-icons/explosion)
- [Stop sign icon](static/img/banned.png) created by [Freepik - Flaticon](https://www.flaticon.com/free-icons/stop-sign)
- [Confusion icon](static/img/confusion.png) created by [Freepik - Flaticon](https://www.flaticon.com/free-icons/confusion)


### Code

- [Secret Key Generation](#secret-key-generation) courtesy of [Humberto Rocha](https://humberto.io/blog/tldr-generate-django-secret-key/)
 
