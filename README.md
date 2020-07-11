Octue.com on Wagtail
====================

[![Build Status](https://travis-ci.com/octue/planex-cms.svg?branch=master)](https://travis-ci.com/octue/planex-cms)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

This project is the backend CMS for [www.octue.com](https://www.octue.com). The [Front-end](https://github.com/octue/planex/) is built with Gatsby and consumes the CMS's content via GraphQL.

Setup
-----

### Installation

Run the following commands:

```bash
python manage.py createcachetable
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 0.0.0.0:8000
```

After the installation the app will accessible on the host machine as http://localhost:8000/admin. The codebase is located on the host
machine an exported to the VM as a shared folder. Code editing and Git operations will generally be done on the host.


### Download production data and media to local VM

```
heroku login
fab pull-production-data
fab pull-production-media
```

You may need to check on Heroku dashboard (https://dashboard.heroku.com) if you have the permission to access the `planex-cms` app.


Site Architecture
-----------------

In this project Wagtail is used as a headless CMS and its data is consumed via [GraphQL](https://graphql.org/). This means that to preview any UI changes on the site you'll also need to setup the [frontend](https://github.com/octue/planex/) component. Wagtail front-end URLs are only accessible by the logged-in users to avoid unauthorised access.

### What's different here?

Any Django/Wagtail specific development is done as usual (Models, Snippets, Taxonomies etc). The difference is in how this data is accessed. Instead of using data in a django template, we explicity define what data is available to query via GraphQL in the `planex/graphql/schema.py` file. If you have done any work with [Graphene](https://docs.graphene-python.org/en/latest/) before then this file will look fairly standard, if not, please take a look through this [simple demo](https://docs.graphene-python.org/projects/django/en/latest/tutorial-plain/) to improve your understanding of how to build on the GraphQL api.


### ...and the frontend?

As mentioned above, the [front-end](https://github.com/octue/planex/) is a separate project built with [Gatsby](https://www.gatsbyjs.org/). You can find out more about Gatsby [here](https://www.gatsbyjs.org/docs/behind-the-scenes/), but the basic concept is that Gatsby is a modern static site builder for React that enables you to build blazingly fast sites while keeping the 'reactness' of a React app.

The HTML of each page is generated in node during the build process. This means when the user opens the page in a browser, the page renders instantly (because it isn't reliant on JS to bootstrap the page, the HTML is ready to go!) but when JS executes on the page everything becomes dynamic like a traditional React app.


### Where does it live?

This project (the backend) is deployed on heroku and is automatically deployed when the `master` branch is updated. The frontend is hosted on [Netlify](https://www.netlify.com/) and is also linked to the frontend repo for auto deployment (new netlify builds are also triggered by a page publish in Wagtail). Netlify will also create 'deploy previews' whenever an MR is created so that you can preview your changes before you merge.

The admin for the live site can be found at https://cms.octue.com/admin/
You can run test GraphQL queries at https://cms.octue.com/graphql/

There will be a staging version of the app on Heroku:

Admin: https://cms.staging.octue.com/admin/
GraphQL: https://cms.staging.octue.com/graphql/


### Deployments

Merges to `master` and `staging` will automatically trigger a deployment to the production and staging sites, respectively.


### What order should I develop in?

When developing a new feature such as a Page model (with accompanying UI), the best approach is to build the models and graphql schema with the project running locally. Once you've finished your backend work, start developing the frontend by pointing the Gatsby project at your local GraphQL endpoint. Once both sides of the feature are done, get your backend reviewed and deployed to Production/Staging. Once your backend is public you can then submit your front-end code for review because Netlfiy will be able to build a preview of the branch with the correct data (The gatsby build will fail if the GraphQL queries don't match up with the backend).