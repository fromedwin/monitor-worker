
# If ./.env file exist, we export variables to current system to display later
if [ -f .env ]; then
  export $(echo $(cat .env | sed 's/#.*//g'| xargs) | envsubst)
fi

# Set default port to access dashboard
if [[ -z "${SERVER}" ]]; then export SERVER=localhost:8000
fi


docker-compose down

