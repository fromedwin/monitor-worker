> **Warning**  
> 
> This project is **alpha** quality. We don't yet guarantee stability, data integrity or a clean upgrade path. Only use this project if you are interested in experimenting with it.

# Monitor-worker fromedwin

This project is a worker for the monitor [fromedwin project](https://github.com/fromedwin/monitor).

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/fromedwin/monitor-client/blob/main/LICENSE)

## Installation

[Docker](https://www.docker.com/) and [Docker-compose](https://docs.docker.com/compose/) are required to run this project.

### Dependancies

```bash
  sudo apt install python3-pip apache2-utils
```

## Run Locally

Clone the project

```bash
  git clone https://github.com/fromedwin/monitor-worker.git
```

Go to the project directory

```bash
  cd monitor-worker
```

Start the server

```bash
  ./run.sh
```
  
## Environment Variables

No variables are required to run locally, but might be needed to configure your production environment

You will need to add the following environment variables to your `.env` file

`PORT` *(default: 8001)* Port used for http 

`PORT_HTTPS` Port used for https

`SERVER_PROTOCOL`  *(default: https)* protocol used to fetch server APIs

`SERVER`  *(default: localhost:8000)* url to fetch server APIs to regsiter (run lcoally outside of docker)

`WEBAUTH_USERNAME` username to protect none public access

`WEBAUTH_PASSWORD` password to protect none public access

`URL` url used to access application

## NGINX

Add extra entrypoint to install `logrotate` on start and start `crond`.

Define nginx configuration from `logrotate/docker-nginx` within `/etc/logrotate.d/nginx`.

Override `bin` using `nginx/logrotate/logrotate.sh` as `/etc/conf.d/logrotate`.

## Feedback

If you have any feedback, please reach out to us at fromedwin@sebastienbarbier.com

  
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Resources

- [Awesome Prometheus Rules](https://awesome-prometheus-alerts.grep.to/rules.html)
