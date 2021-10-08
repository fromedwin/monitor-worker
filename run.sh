# Install python dependancies
pip3 install -r requirements.txt

# If ./.env file exist, we export variables to current system to display later
if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
fi

# Set default port to access monitor-client web interface
if [[ -z "${PORT}" ]]; then export PORT=8001
fi
# Set protocol to load nginx
if [[ -z "${PROTOCOL}" ]]; then export PROTOCOL=http
fi
# Set default username for web auth
if [[ -z "${WEBAUTH_USERNAME}" ]]; then export WEBAUTH_USERNAME=$(openssl rand -base64 12)
fi
# Set default password for webauth
if [[ -z "${WEBAUTH_PASSWORD}" ]]; then export WEBAUTH_PASSWORD=$(openssl rand -base64 12)
fi

# GENERATE PASSWORD
echo "Generate user: $WEBAUTH_USERNAME $WEBAUTH_PASSWORD"
htpasswd -cmb .htpasswd $WEBAUTH_USERNAME $WEBAUTH_PASSWORD

echo "Register"
python3 scripts/register.py

# IF register.py fail
if [ $? -ne 0 ]; then
	exit
fi

mkdir -p prometheus/alerts

echo "Load-config"
python3 scripts/load_config.py

# IF load-config.py return code 0
if [ $? -ne 0 ]; then
	exit
fi

if [[ $@ == *"-prod"* ]]; then

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
    docker-compose up -d
  fi

else

  if [[ $@ == *"-d"* ]]; then

  	docker-compose up -d

    # IF load-config.py return code 0
    if [ $? -ne 0 ]; then
      echo "❌ Docker might not be running."
      exit
    fi

  	echo "Access prometheus at localhost:$PORT"

  else
    docker-compose up
  fi

fi