#!/bin/bash

echo '▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄'
echo '█░▄▄█░▄▄▀█▀▄▄▀█░▄▀▄░█░▄▄█░▄▀█░███░██▄██░▄▄▀'
echo '█░▄██░▀▀▄█░██░█░█▄█░█░▄▄█░█░█▄▀░▀▄██░▄█░██░'
echo '█▄███▄█▄▄██▄▄██▄███▄█▄▄▄█▄▄███▄█▄██▄▄▄█▄██▄'
echo '▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀'

echo '🟢 - Install dependencies ⚙️'
# Install python dependancies
pip3 install -r requirements.txt

echo '🟢 - Load .env file'
touch .env # Will creat .env if it does not exist
source .env # Load .env variables

# Set default port to access monitor-client web interface
if [[ -z "${PORT}" ]]; then export PORT=8001
fi
# Set protocol to load nginx
if [[ -z "${PROTOCOL}" ]]; then export PROTOCOL=http
fi

echo '🟢 - Generate user credentials for .htpasswd'
# Set default username for web auth
if [[ -z "${WEBAUTH_USERNAME}" ]]; then export WEBAUTH_USERNAME=$(openssl rand -base64 12)
fi
# Set default password for webauth
if [[ -z "${WEBAUTH_PASSWORD}" ]]; then export WEBAUTH_PASSWORD=$(openssl rand -base64 12)
fi
echo "  👤 username: $WEBAUTH_USERNAME"
echo "  🔐 password: $WEBAUTH_PASSWORD"
htpasswd -cmb .htpasswd $WEBAUTH_USERNAME $WEBAUTH_PASSWORD

echo "🟢 - Register worker to main server"
python3 scripts/register.py

# IF register.py fail
if [ $? -ne 0 ]; then
  echo "🔴 - See error bellow"
	exit
fi

echo "🟢 - Load config prometheus"
mkdir -p prometheus/alerts
mkdir -p alertmanager
python3 scripts/load_config.py

# IF load-config.py return code 0
if [ $? -ne 0 ]; then
  echo "🔴 - See error bellow"
	exit
fi


if [[ $@ == *"-prod"* ]]; then

  echo "🟢 - 🚀💰 - Start as production instance"
  export NGINX="production" # Will load nginx/production/*.conf files

  if [[ $DOMAIN == *"localhost"* ]]; then
    echo 'You need to define a custom domain other than localhost or host.docker.internal'
    exit
  fi

  if [[ $DOMAIN == *"host.docker.internal"* ]]; then
    echo 'You need to define a custom domain other than localhost or host.docker.internal'
    exit
  fi

  if [[ -z "${MAIL}" ]]; then 
    echo 'Defining MAIL env var is required'
    exit
  fi

  # Set STAGING to 1 if you're testing your setup to avoid hitting request limits
  if [[ -z "${STAGING}" ]]; then 
    export STAGING=0
    echo '⚠️ Running lets-encrypt staging with potential request limits'
  fi
  
  if [[ $@ == *"-cert"* ]]; then
    source scripts/init-letsencrypt.sh
  else
    docker-compose --profile prod up -d
  fi

else
  echo "🟢 - 🚀🧑‍💻 - Start as development instance"
  echo "Access prometheus at localhost:$PORT"

  if [[ $@ == *"-d"* ]]; then

    echo "Run as deamon"

  	docker-compose up -d

    # IF load-config.py return code 0
    if [ $? -ne 0 ]; then
      echo "🔴 Docker might not be running."
      exit
    fi

  else
    echo "⚠️ Running as main thread (use -d to run as deamon)"
    docker-compose up
  fi

fi