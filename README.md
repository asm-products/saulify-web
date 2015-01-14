## Saulify for Web

[![Build Status](https://travis-ci.org/asm-products/saulify-web.svg?branch=master)](https://travis-ci.org/asm-products/saulify-web) 
<a href="https://assembly.com/saulify/bounties"><img src="https://asm-badger.herokuapp.com/saulify/badges/tasks.svg" height="24px" alt="Open Tasks" /></a>

Got a hard-to-read website? [Better call Saul](http://saulify.me) to clean it up!

Saulify runs on Heroku: [http://saulify.heroku.com](http://saulify.heroku.com)

#### Installing Locally

Saulify is built on [Python](https://www.python.org/) using the [Flask](http://flask.pocoo.org/docs/0.10/) micro-framework. 

To install it locally:

- [Clone this Github repo](https://help.github.com/articles/fetching-a-remote/) to your local computer.
- Install [Heroku Toolbelt](https://toolbelt.heroku.com/) and ensure you create a Heroku account if you don't have one already.
- Install [virtualenv-burrito](https://github.com/brainsik/virtualenv-burrito) to install a tool for managing your Python virtual environments.
- Use `mkvirtualenv saulify` to create a new virtual environment for the project. This will ensure all of your Python libraries are installed properly without conflict.
- Use `cd <saulify folder path>` to change to the Saulify directory and then `workon saulify` to switch to the Saulify virtual environment you created previously.
- Use `pip install -r requirements.txt` to install the 3rd party dependencies, such as Flask, et. al.
- Set up a `.env` file in the root Saulify directory with the environment variables taken from the Heroku config: https://devcenter.heroku.com/articles/config-vars (Ask a team member to send you the file if you don't have access)
- Type `foreman run python runserver.py` (for development) or `foreman start` (for production) at the command line to start the local server.

Note: Saulify uses the [Newspaper](https://github.com/codelucas/newspaper) library as a backup for scraping website articles that we don't have scraping recipes for. If you have trouble installing it on Mac OS X Yosemite during the `pip install` process above, please see this [Github issue](https://github.com/codelucas/newspaper/issues/79) for helpful info.

More info here for [getting started w/ Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python-o).

#### Scraping

Saulify uses Instapaper style recipes for scraping each article based on the domain of the article. 

These recipes are open source and can be found here: [https://github.com/fivefilters/ftr-site-config](https://github.com/fivefilters/ftr-site-config) and within the `/sitespecs` directory of the repo. (See below for a means to test these sitespecs.)

If you'd like to generate a new domain recipe, you can use the [point-and-click tool the FiveFilters team has provided](http://siteconfig.fivefilters.org) for getting the xpaths of each page section you'd like to scrape or exclude. More help on the format can be found [here](http://help.fivefilters.org/customer/portal/articles/223153-site-patterns).

If we cannot find a proper recipe for a domain, we use the [Newspaper](https://github.com/codelucas/newspaper) library as a backup which uses heuristics instead of recipes.

#### Testing

Saulify uses the [pytest](http://pytest.org) framework for making sure we keep clear of new bugs and regressions and these tests can be found in the `/tests` directory. 

You'll need to set an `.env` variable for the `TEST_DATABASE_URL` to be a local or remote database that you want to use specifically for testing.

Then you can run the test suite via the command line using:

```shell
$ foreman run py.test
```

Also, we have a secondary test script for verifying the accuracy of the article scraper recipes. You can run that script via the command line using:

```shell
$ python runreport.py 2> /dev/null
```

where `2> /dev/null` suppresses any exception warnings so the output is a bit clearer.

You can also use the `-v` flag to have verbose output with URLs and detailed failure messages shown for each test.

#### Contributing

This is a product being built by the Assembly community. If you'd like to contribute to Saulify, we'd love to have the help! 

Please follow these steps:

- Go to [https://assemblymade.com/saulify](https://assemblymade.com/saulify) and sign up for an Assembly account.
- Link your GitHub account to your Assembly account in your profile settings.
- Fork this repo [asm-products/saulify-web](https://github.com/asm-products/saulify-web)
- [Find a bounty](https://assembly.com/saulify/bounties) you'd like to work on (or create a new one) and commit your code to your fork
- Open up a new pull request on Github into the `development` branch and let us know what bounty the code changes are for.
- We'll review the code, give any feedback, merge it, and award you the bounty (which gives you ownership over Saulify)!

===

#### Made by Assembly

Assembly products are like open-source and made with contributions from the community. Assembly handles the boring stuff like hosting, support, financing, legal, etc. Once the product launches we collect the revenue and split the profits amongst the contributors.

Visit [https://assembly.com](https://assembly.com) to learn more.
