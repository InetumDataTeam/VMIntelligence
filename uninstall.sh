docker kill $(docker ps -q)
docker system prune -af
docker volume rm -f vmintelligence_pgdata
