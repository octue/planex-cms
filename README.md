planex-cms: A capable headless CMS based on Wagtail
====================

[![Build Status](https://travis-ci.com/octue/planex-cms.svg?token=ZfRed1JDegwQ9HCopiWT&branch=master)](https://travis-ci.com/octue/planex-cms)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/octue/planex-cms)

This project is the backend CMS for [www.octue.com](https://www.octue.com).

**PROJECT STATUS**

The next job is to refactor the existing Material-UI based page system for [octue.com](www.octue.com) out of its current private repo and into [the planex repo](https://github.com/octue/planex/), to consume content from `planex-cms` via `GraphQL`, then automate build/deploy with Gatsby.

Quick-start
-----------

One-click deploy to heroku using the button above. It'll run on the free tier, but its best to use hobby tier because:
 - You get SSL (everything on https:// not http://) which avoids your login details being sent unencrypted over the internet (!)
 - If your frontend uses forms, the server needs to be always-on to receive the form submissions

You can access it at whatever URL heroku gives you - choosing the free tier with a hobby database is fine for now!

If you wish, sign into your domain name provider and, point `https://cms.your-domain.com` to your heroku app ([here's how](https://medium.com/@imranhsayed/adding-your-custom-domain-to-heroku-app-cdd68d2db67f)).


Development
-----------

To actually develop this repo (or your fork of it), [install docker](https://docs.docker.com/engine/install/), then run the following commands:

```bash
plx manage createcachetable
plx manage migrate
plx manage collectstatic
plx manage createsuperuser
plx manage "init_cms --user <the superuser email you just created>"
plx dev
```

After the installation the content management system will accessible on the host machine as http://localhost:8000/.


Site Architecture
-----------------

In this project Wagtail is used as a headless CMS, which also serves documents and images.
Its data is consumed via [GraphQL](https://graphql.org/).

To turn this into a viewable site, you'll also need to setup the [frontend](https://github.com/octue/planex/). Wagtail
front-end URLs are only accessible by the logged-in users to avoid unauthorised access.

### What's different here?

Any Django/Wagtail specific development is done as usual (Models, Snippets, Taxonomies etc). The difference is in how this data is accessed. Instead of using data in a django template, we explicity define what data is available to query via GraphQL in the `planex/graphql/schema.py` file. If you have done any work with [Graphene](https://docs.graphene-python.org/en/latest/) before then this file will look fairly standard, if not, please take a look through this [simple demo](https://docs.graphene-python.org/projects/django/en/latest/tutorial-plain/) to improve your understanding of how to build on the GraphQL api.


### ...and the frontend?

As mentioned above, the [front-end](https://github.com/octue/planex/) is a separate project built with [Gatsby](https://www.gatsbyjs.org/). You can find out more about Gatsby [here](https://www.gatsbyjs.org/docs/behind-the-scenes/), but the basic concept is that Gatsby is a modern static site builder for React that enables you to build blazingly fast sites while keeping the 'reactness' of a React app.

The HTML of each page is generated in node during the build process. This means when the user opens the page in a browser, the page renders instantly (because it isn't reliant on JS to bootstrap the page, the HTML is ready to go!) but when JS executes on the page everything becomes dynamic like a traditional React app.


### Where does it live?

This project (the backend) is deployed on heroku and is automatically deployed when the `master` branch is updated. The frontend is hosted on [Netlify](https://www.netlify.com/) and is also linked to the frontend repo for auto deployment (new netlify builds are also triggered by a page publish in Wagtail). Netlify will also create 'deploy previews' whenever an MR is created so that you can preview your changes before you merge.

The admin for the live site can be found at https://cms.octue.com/
You can run test GraphQL queries at https://cms.octue.com/graphql/


### What order should I develop in?

When developing a new feature such as a Page model (with accompanying UI), the best approach is to:
 - Build the new models and graphql schema with the project running locally
 - Then develop the frontend by pointing it at your local GraphQL endpoint.
 - Once both sides of the feature are done, get your backend reviewed and deployed.
 - When your backend is public you can then submit your front-end code for review because Netlfiy will be
 able to build a preview of the branch with the correct data (The gatsby build will fail if the GraphQL queries don't
 match up with the backend).
