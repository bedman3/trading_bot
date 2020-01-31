if (which docker-compose)
then
  DOCKER_COMPOSE_BIN="$(which docker-compose)"
else
  DOCKER_COMPOSE_BIN=/opt/bin/docker-compose
fi

$DOCKER_COMPOSE_BIN down
docker pull registry.gitlab.com/bedman3/trading_bot/trading_bot:latest
$DOCKER_COMPOSE_BIN up -d