docker run -d -h trading-bot-rabbitmq --name trading-bot-rabbitmq -e RABBITMQ_DEFAULT_USER=<username> -e RABBITMQ_DEFAULT_PASS=<password> -p 8080:15672 rabbitmq:3-management
