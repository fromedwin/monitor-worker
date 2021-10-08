#!/bin/bash

if ! [ -x "$(command -v docker-compose)" ]; then
  echo 'Error: docker-compose is not installed.' >&2
  exit 1
fi

# domains=(sebastienbarbier.com www.sebastienbarbier.com)
domains=($DOMAIN)
rsa_key_size=4096
data_path="./certbot"
email=$MAIL # Adding a valid address is strongly recommended
staging=$STAGING # Set to 1 if you're testing your setup to avoid hitting request limits
folder="monitor" # Change needs to be reported to nginx/remote/nginx.conf path to certificate

if [ -d "$data_path" ]; then
  read -p "Existing data found for $domains. Continue and replace existing certificate? (y/N) " decision
  if [ "$decision" != "Y" ] && [ "$decision" != "y" ]; then
    exit
  fi
fi


if [ ! -e "$data_path/conf/options-ssl-nginx.conf" ] || [ ! -e "$data_path/conf/ssl-dhparams.pem" ]; then
  echo "### Downloading recommended TLS parameters ..."
  mkdir -p "$data_path/conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "$data_path/conf/options-ssl-nginx.conf"
  curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "$data_path/conf/ssl-dhparams.pem"
  echo
fi

echo "### Creating dummy certificate for $domains ..."
path="/etc/letsencrypt/live/$folder"
mkdir -p "$data_path/conf/live/$folder"
sudo docker-compose run --rm --entrypoint "\
  openssl req -x509 -nodes -newkey rsa:4096 -days 1\
    -keyout '$path/privkey.pem' \
    -out '$path/fullchain.pem' \
    -subj '/CN=localhost'" certbot
echo


echo "### Starting nginx ..."
sudo docker-compose up --force-recreate -d nginx
echo

echo "### Deleting dummy certificate for $domains ..."
sudo docker-compose run --rm --entrypoint "\
  rm -Rf /etc/letsencrypt/live/$folder && \
  rm -Rf /etc/letsencrypt/archive/$folder && \
  rm -Rf /etc/letsencrypt/renewal/$folder.conf" certbot
echo


echo "### Requesting Let's Encrypt certificate for $domains ..."
#Join $domains to -d args
domain_args=""
for domain in "${domains[@]}"; do
  domain_args="$domain_args -d $domain"
done

# Select appropriate email arg
case "$email" in
  "") email_arg="--register-unsafely-without-email" ;;
  *) email_arg="--email $email" ;;
esac

# Enable staging mode if needed
if [ $staging != "0" ]; then staging_arg="--staging"; fi

docker-compose run --rm --entrypoint "\
  certbot certonly --webroot -w /var/www/certbot \
    $staging_arg \
    $email_arg \
    $domain_args \
    --rsa-key-size $rsa_key_size \
    --agree-tos \
    --force-renewal" certbot
echo

## Create symbolic link give nginx access to generated certificate
ln -sf $DOMAIN ./certbot/conf/live/monitor

echo "### Reloading nginx ..."
docker-compose exec nginx nginx -s reload
