[![Actions Status](https://github.com/MBohdan/yamdb_final/workflows/yamdb_final_workflow/badge.svg)](https://github.com/MBohdan/yamdb_final/actions)
![Yamdb_Final](https://img.shields.io/github/workflow/status/MBohdan/yamdb_final/yamdb_final_workflow)


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
