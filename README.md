### Saulify for Web
===

Got a hard-to-read website? [Better call Saul](http://saulify.me) to clean it up!

Saulify runs on Heroku: [http://saulify.heroku.com](http://saulify.heroku.com)

#### Installing Locally

Saulify is built on [Python](https://www.python.org/) using the [Flash](http://flask.pocoo.org/docs/0.10/) micro-framework. 

To install it:

- [Clone this Github repo](https://help.github.com/articles/fetching-a-remote/) to your local computer.
- Install [Heroku Toolbelt](https://toolbelt.heroku.com/) and ensure you create a Heroku account if you don't have one already.
- Install [virtualenv-burrito](https://github.com/brainsik/virtualenv-burrito) to install a tool for managing your Python virtual environments.
- Use `mkvirtualenv saulify` to create a new virtual environment for the project. This will ensure all of your Python libraries are installed properly without conflict.
- Use `cd <saulify folder path>` to change to the Saulify directory and then `workon saulify` to switch to the Saulify virtual environment you created previously.
- Use `pip install -r requirements.txt` to install the 3rd party dependencies, such as Flask, et. al.
- Type `foreman run python runserver.py` (for development) or `foreman start` (for production) at the command line to start the local server.

Note: Saulify uses the [Newspaper](https://github.com/codelucas/newspaper) library for scraping website articles. If you have trouble installing it on Mac OS X Yosemite during the `pip install` process above, please see this [Github issue](https://github.com/codelucas/newspaper/issues/79) for helpful info.


More info here for [getting started w/ Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python-o).

#### Contributing

This is a product being built by the Assembly community. If you'd like to contribute to Saulify, we'd love to have the help! 

Please follow these steps:

- Go to [https://assemblymade.com/saulify](https://assemblymade.com/saulify) and sign up for an Assembly account.
- Link your GitHub account to your Assembly account in your profile settings.
- Fork this repo [asm-products/saulify-web](https://github.com/asm-products/saulify-web)
- [Find a bounty](https://assembly.com/saulify/bounties) you'd like to work on (or create a new one) and commit your code to your fork
- Open up a new pull request on Github and let us know what bounty the code changes are for.
- We'll review the code, give any feedback, merge it, and award you the bounty!

===

#### Made by Assembly

Assembly products are like open-source and made with contributions from the community. Assembly handles the boring stuff like hosting, support, financing, legal, etc. Once the product launches we collect the revenue and split the profits amongst the contributors.

Visit [https://assembly.com](https://assembly.com) to learn more.
