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
# Set default port to access dashboard
if [[ -z "${SERVER}" ]]; then export SERVER=localhost:8000
fi

echo "Register"
python3 scripts/register.py

# IF register.py fail
if [ $? -ne 0 ]; then
	exit
fi

echo "Load-config"
python3 scripts/load-config.py

# IF load-config.py return code 0
if [ $? -ne 0 ]; then
	exit
fi

docker-compose up

echo "Access prometheus at localhost:$PORT"
