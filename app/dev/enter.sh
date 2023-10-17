source env/bin/activate

export localhost_ip="$(hostname -I | awk '{print $1}')"

export environment="local"
echo "local-ip: [$localhost_ip] | environment: [$environment]"

export API_NAME="edmachine"
export DB_HOST="localhost"
export DB_USER="root"
export DB_PASS="root"
export DB_NAME="edmachine"
export DB_PORT="3307"