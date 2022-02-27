cd "$(dirname "$0")" || exit 1
docker-compose up -d
echo 'Enter any charachter to bring down queue'
read -r var
docker-compose down -v
