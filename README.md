# Agreelance group 12
[![Heroku](https://pyheroku-badge.herokuapp.com/?app=agreelance-group12&style=flat-square)](https://agreelance-group12.herokuapp.com/)
[![pipeline status](https://gitlab.com/tdt4242-project/agreelance/badges/master/pipeline.svg?style=flat-square)](https://gitlab.com/tdt4242-project/agreelance/-/commits/master)
[![License](http://img.shields.io/:license-mit-blue.svg?style=flat-square)](http://badges.mit-license.org)

The best way to agree on the price of your freelancing jobs!

Application available at: https://agreelance-group12.herokuapp.com

## Users
Username | Password | Description
---|---|---
Bjarte|SwokT2!5LoSf| Superuser status
Eirik|SwokT2!5LoSf|
Seb|SwokT2!5LoSf|

## Git flow
We use the following branching strategy in this project
### Master Branch: `master`

We consider `master` to be the main branch where the source code of `HEAD` **always reflects a stable application**. This is the branch from which all `feature` branches are forked, and into which all `feature` branches are merged.

Changes to `master` should always come through a **pull request**!

### Feature Branches: `feature-*`

Feature branches are used to develop new features. The essence of a feature branch is that it exists as long as the feature is in development, but will eventually be merged back into master (to definitely add the new feature to the upcoming release) or discarded (in case of a disappointing experiment).

Feature branches should not exist in `origin` for very long. They should be merged into `master`, via pull request, as quickly as possible and then cleaned up.

- Naming convention: `feature-*`
- Branches from: `master`
- Must merge back into: `master`

## Code and structure
- **agreelance/** django project folder containing the project modules
  - **core/** contains all the project templates
    - **index.html** One of the project templates that uses a template language to insert if, loops and variables into html.
  - **home/** user profile - overview over user projects
    - **static/** - contains static files like js and images
    - **templatetags/** folder containing [template tags](https://docs.djangoproject.com/en/2.1/ref/templates/builtins/). Methods you import into your templates. Can be used in combination with views.
    - **admins.py** - file contaning definitions to connect models to the django admin panel
    - **urls.py** - contains mapping between urls and views
    - **models.py** - contains data models
    - **tests/** - contains tests for the module. [View Testing in Django](https://docs.djangoproject.com/en/2.1/topics/testing/) for more.
    - **views.py** - Controller in MVC. Methods for rendering and accepting user data
    - **forms.py**  -  defenition of forms. Used to render html forms and verify user input
  - **payment/** - module handling payment
  - **projects/** - The largest module of the project containing code for creating project and tasks. Upload files, view files, adding roles and user to roles.
  - **agreelance/** - The projects main module contaning settings.
  - **static/** - common static files
  - **user/** - module extending django's user model with a profile contaning more information about the user.
  - **manage.py** - entry point for running the project.
  - **seed.json** - contains seed data for the project to get it up and running quickly

## Testing
To run the relevant tests for this project (user and projects module), run the following command from the root folder:

`python manage.py test projects/tests user/tests`

### Coverage
You can run coverage.py to get code coverage reports. To run the tests related to the users and projects modules, run the following commands from the root folder:

```
coverage run --source="./projects" manage.py test projects/tests
coverage run --source="./user" manage.py test user/tests
coverage html
```

A nicely presented coverage report (HTML files) will then be available in the htmlcov folder in the root of your directory. NB: The htmlcov folder is gitignored (as it should be). So you will not find these find int the GitLab repository.

## Get started
It's reccomended to have a look at: https://www.djangoproject.com/start/

Basic tutorial that walks trough what the different files do.
https://docs.djangoproject.com/en/2.0/intro/tutorial01/

Create a virtualenv https://docs.python-guide.org/dev/virtualenvs/


## Local setup

### Installation with examples for ubuntu. Windows and OSX is mostly the same

Fork the project and clone it to your machine.

#### Setup and activation of virtualenv (env that prevents python packages from being installed globaly on the machine)
Naviagate into the project folder.

`pip install virtualenv`

`virtualenv env`

For mac/linux:

`source env/bin/activate`

For windows:

`env\Scripts\activate.bat`

If you get an error related to charmap on Windows, run this command:
`set PYTHONIOENCODING=UTF-8`


#### Install python requirements

`pip install -r requirements.txt`

**Note: Mac users may get an error related to psycopg2. To fix this try running:**

`pip install psycopg2==2.7.5`


#### Migrate database

`python manage.py migrate`


#### Create superuser

Create a local admin user by entering the following command:

`python manage.py createsuperuser`

Only username and password is required


#### Start the app

`python manage.py runserver`


#### Add initial data

You can add initial data either by going to the url the app is running on locally and adding `/admin` to the url.

Add some categories and you should be all set.

Or by entering 

`python manage.py loaddata seed.json`


## Email
Copy `agreelance/local_settings_example.py` to `agreelance/local_settings.py` and replace the email placeholder values with values dscribes in the email section later in the instructions.

To support sending of email you will have to create a gmail account and turn on less secure apps. *Do not use your own email as Google might lock the account*. See https://support.google.com/accounts/answer/6010255?hl=en for instructions for turning on less secure apps.

To get email working on heroku you might have to visit https://accounts.google.com/DisplayUnlockCaptcha and click `continue` as the heroku server is in another location and Google thinks it is a hacking attempt. 

## Continuous integration
Continuous integration will build the code pushed to master and push it to your heroku app so you get a live version of your latest code by just pushing your code to GitLab.

1. Fork the project at GitLab
2. Create a heroku account and an app.
3. Set the project in the .gitlab-cs.yml file by replacing `<Your-herokuproject-name>` with the name of the Heroku app you created
`- dpl --provider=heroku --app=<Your-herokuproject-name> --api-key=$HEROKU_STAGING_API_KEY`
4. Set varibles at GitLab
    * settings > ci > Environment Variables
    * `HEROKU_STAGING_API_KEY` = heroku > Account Settings > API Key
4. Add heroku database
   * Resources > Add ons > search for postgres > add first option
5. Set variables at heroku. Settings > Config vars > Reveal vars
   * `DATABASE_URL` = Should be set by default. If not here is where you can find it: Resources > postgress > settings > view credentials > URI
   * `EMAIL_HOST_PASSWORD` email password. Not mandatory if you do not want to send email
   * `EMAIL_HOST_USER` email adress. Not mandatory if you do not want to send email
   * `IS_HEROKU` = `IS_HEROKU`
6. On GitLab go to CI / CD in the repository menu and select `Run Pipeline` if it has not already started. When both stages complete the app should be available on heroku. Staging will fail from timeout as Heroku does not give the propper response to end the job. But the log should state that the app was deployed.
7. Setup the applications database.
  * Install heroku CLI by following: https://devcenter.heroku.com/articles/heroku-cli
  * Log in to the Heroku CLI by entering `heroku login`. This opens a webbrowser and you accept the login request.
  * Migrate database by entering
  `heroku run python manage.py migrate -a <heroku-app-name>`. `Heroku run` will run the folowing command on your heroku instance. Remember to replace `<heroku-app-name>` with your app name
  * and create an admin account by running
  `heroku run python manage.py createsuperuser -a <heroku-app-name>`.
  * seed database `heroku run python manage.py loaddata seed.json -a <heroku-app-name>`

### Reset Database
`heroku pg:reset DATABASE_URL -a <heroku-app-name>`

## Data seeding
The data seed provided contains 3 users, described in Users section above
