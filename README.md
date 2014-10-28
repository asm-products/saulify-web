### Saulify for Web
===

Got a hard-to-read website? [Better call Saul](http://saulify.me) to clean it up!

#### Installing

Saulify is built on [Python](https://www.python.org/) using the [Flash](http://flask.pocoo.org/docs/0.10/) micro-framework. 

To install it:

- [Clone this Github repo](https://help.github.com/articles/fetching-a-remote/) to your local computer.
- Install [Heroku Toolbelt](https://toolbelt.heroku.com/) and ensure you create a Heroku account if you don't have one already.
- Install [virtualenv-burrito](https://github.com/brainsik/virtualenv-burrito) to install a tool for managing your Python virtual environments.
- Use `mkvirtualenv saulify` to create a new virtual environment for the project. This will ensure all of your Python libraries are installed properly without conflict.
- Use `cd <saulify folder path>` to change to the Saulify directory and then `workon saulify` to switch to the Saulify virtual environment you created previously.
- Use `pip install -r requirements.txt` to install the 3rd party dependencies, such as Flask, et. al.
- Type `foreman start` at the command line to start the local server.

More info here for [getting started w/ Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python-o).

===

#### Made by Assembly

This is a product being built by the Assembly community. You can help push this idea forward by visiting [https://assembly.com/saulify](https://assembly.com/saulify).

Assembly products are like open-source and made with contributions from the community. Assembly handles the boring stuff like hosting, support, financing, legal, etc. Once the product launches we collect the revenue and split the profits amongst the contributors.

Visit [https://assembly.com](https://assembly.com) to learn more.
