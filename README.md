# LITReview

This project is a web application developped with the [Django web framework](https://www.djangoproject.com/) and [bootstrap5](https://getbootstrap.com/). It is a book review social platform.

Users of the app can create tickets to ask for a specific book review, they can post review in reply to someone else's ticket, and they can follow one another.

The app has 4 sections:

  * signup / signin pages
  * user's flow (latest tickets/review from who the user is following)
  * user's posts where the user can see what he has posted, then edit or delete any post
  * user follows page that lists the user's followers and followings, the user might sub to a new user or unsub from a following
 
## Setup
  
The first step is to clone this repo.

```
$ git clone https://github.com/bdibon/litreview.git
```

Then you want to install `pipenv` on your machine if you don't already have it.

```
$ pip install --user pipenv
```

From the project's root directory, install the project's dependencies.

```
$ pipenv install --dev
```

Finally, activate the virtual environment and start the server.

```
$ pipenv shell
$ py manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
February 21, 2022 - 12:07:12
Django version 4.0.2, using settings 'litreview.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Notes

This project has not been setup to be deployed to production, it is still in **development flow** so no real database has been plugged in nor any containerization or specific settings regarding static assets.
