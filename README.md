
# Monitor-client fromedwin

This project is a monitoring client for the monitor [fromedwin project]().


## Installation

[Docker](https://www.docker.com/) and [Docker-compose](https://docs.docker.com/compose/) are required to run this project.
## Run Locally

Clone the project

```bash
  git clone https://github.com/fromedwin/monitor-client.git
```

Go to the project directory

```bash
  cd monitor-client
```

Start the server

```bash
  ./run.sh
```
  
## Environment Variables

No variables are required to run locally, but might be needed to configure your production environment

You will need to add the following environment variables to your `.env` file

`PORT` *(default: 8001)*

`SERVER_PROTOCOL` url used to generate letsencrypt SSL certificate and access the application

`SERVER` secret key used by django's session

`WEBAUTH_USERNAME` username to protect none public access

`WEBAUTH_PASSWORD` password to protect none public access

  
## Feedback

If you have any feedback, please reach out to us at fromedwin@sebastienbarbier.com

  
## License

[MIT](https://choosealicense.com/licenses/mit/)


## Resources

- [Awesome Prometheus Rules](https://awesome-prometheus-alerts.grep.to/rules.html)
