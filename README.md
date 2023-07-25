# Monitor-worker fromedwin

This project is a worker for the monitor [fromedwin project](https://github.com/fromedwin/monitor).

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/fromedwin/monitor-client/blob/main/LICENSE)

## Installation

[Docker](https://www.docker.com/) and [Docker-compose](https://docs.docker.com/compose/) are required to run this project.

### Dependancies

This project

```bash
  sudo apt install python3-pip apache2-utils
```

## Development environment

```bash
  git clone https://github.com/fromedwin/monitor-worker.git
  cd monitor-worker
  ./run.sh
```

## Environment Variables

No variables are required to run locally, but might be needed to configure your production environment

You will need to add the following environment variables to your `.env` file

`SERVER_URL` (default `http://host.docker.internal:8000`): URL to reach [fromedwin/monitor](https://github.com/fromedwin/monitor) instance.

`WORKER_URL` (default `http://localhost:8001`): Worker needs to be reach by the server, this is the url used to generated the https certificate.

`WEBAUTH_USERNAME` (optional) username to protect none public access. If none, it is randomly generated.

`WEBAUTH_PASSWORD` (optional) password to protect none public access. If none, it is randomly generated.

`DISABLE_MONITORING` (default False) disable availability monitoring

`DISABLE_PERFORMANCE` (default False) disable performance monitoring

## Nginx logs

Add extra entrypoint to install `logrotate` on start and start `crond`.

Define nginx configuration from `logrotate/docker-nginx` within `/etc/logrotate.d/nginx`.

Override `bin` using `nginx/logrotate/logrotate.sh` as `/etc/conf.d/logrotate`.

## Deploy to production

```bash
  git clone https://github.com/fromedwin/monitor-worker.git
  cd monitor-worker
  echo "SERVER_URL=https://server.example.com" >> .env
  echo "WORKER_URL=https://worker.example.com" >> .env
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Resources

- [Awesome Prometheus Rules](https://awesome-prometheus-alerts.grep.to/rules.html)
