#Flask
Flask is the microframework we will start with. If you did the reading from the last class, you are probably ready to go (hint go back and do it if you haven't). However, we will need to do a couple of things to get you started.
1. Install virtualenv if you haven't already - $ sudo easy\_install virtualenv
2. Create a virtualenv in your project folder - $ virtualenv venv
3. Start up virtualenv - $ . vevn/bin/activate
4. Install some packages:
  - $ pip install Flask
  - $ pip install Flask-SQLAlchemy
  - $ pip install MySQL-python

##virtualenv
virtualenv creates a virtual environment, localizing all the things you install to your project - so that they aren't installed for and accessible to everything on your computer. Imagine you were working on two projects that used two versions of the same package. One or both would break. With virtualenv you don't have to worry about conflicts. If your app says you don't have the base packages installed when you try to start it, you probably forgot to activate your venv.

##SQLAlchemy
SQLAlchemy is what we call an **ORM** - object relational model. It connects to the db and helps us query the db and turn the raw data into python objects we can use in our application. Feel free to google it to learn more about what you can do with it. We won't go too far in-depth until we have done some sql curriculum, but you will quickly learn how much work it saves you.

##Templates
Templates are html with some token sets ({{ }} and {% %}) to indicate when we want to insert values and when we want to add some control flow (ifs and loops). There are many template engines, but the most popular for python applications (especially flask) is Jinja2. All engines do basically the same thing - use these tokens and a hash of variables to be passed in for building the html. Read more at http://jinja.pocoo.org/. It is best to keep your templates as simple as possible, any complicated logic should be done in the view function that calls the template engine.
