
[![yamdb_final](https://img.shields.io/github/workflow/status/MBohdan/yamdb_final/yamdb_workflow/badge.svg?style=flat&logo=github&logoColor=white&color=1CA2F1)](https://github.com/MBohdan/yamdb_final/actions)
[![Twitter Badge](https://img.shields.io/badge/Twitter-Profile-informational?style=flat&logo=twitter&logoColor=white&color=1CA2F1)](https://twitter.com/BraydonCoyer)


# My Project 1

One Paragraph of project description goes here

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

How to use application:

```
docker exec api_yamdb_web_1 python manage.py loaddata fixtures.json   #  load fixtures in project
docker exec  -it api_yamdb_web_1 python manage.py createsuperuser --email EMAIL@EMAIL.COM --username MYUSER  # create superuser
docker-compose up -d # Run application
docker-compose down # stop application

```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
