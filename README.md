[![Docker Pulls](https://img.shields.io/docker/pulls/wcarlsen/captains-log.svg)](https://hub.docker.com/r/wcarlsen/captains-log/)
![Docker Cloud Build Status](https://img.shields.io/docker/cloud/build/wcarlsen/captains-log)

# Captain's log :wheel_of_dharma:
A metrics exporter for Kubernetes events. In this project we assume that events older than 5 seconds is old news and we will discard them.

It requires a Kubernetes config file to consume events and for local development you will need Python 3.8 and pipenv installed.

To get started run:

```bash
make install # install dependencies

cp .env.example .env # creating environment variables file

make run # run the service
```
