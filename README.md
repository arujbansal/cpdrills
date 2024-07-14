# cpdrills

CP Drills (Competitive Programming Drills) is a training platform designed to help increase your problem-solving speed by giving you access to several analytics. Since it is no longer being maintained, its source code is open to the public. You can look at [screenshots](#screenshots) below or take a look at the website hosted [here](https://arujbansal.pythonanywhere.com/) but it is likely that you cannot access practice features here. You can download and run the code locally by following the [usage guide](#usage-guide).

## Screenshots

## Usage Guide
1. Clone this repository, create a python virtual environment, and install the requirements:
```
$ pip install -r requirements.txt
```
3. Create a `.env` file using `env_template.txt` and fill in the required fields.
4. Initialise the database:
```
$ python manage.py migrate
$ python manage.py makemigrations
```
5. Create a super user to login to the website:
```
$ python manage.py createsuperuser
```
6. Run the FastAPI server used to query the Codeforces API:
```
$ uvicorn cf_api_server:app --host 0.0.0.0 --port 8080
```
7. Start the django app in the cpdrills directory:
```
$ cd cpdrills
$ python manage.py runserver
```
8. Open the website, login with your superuser account, and add your Codeforces handle to your profile. You may need to navigate to /admin and update your superuser profile's details if you cannot directly save your profile.

Note: If something breaks, it is likely that a path or URL needs to be updated. Just follow the error and change the required paths. Check the FastAPI endpoint.
