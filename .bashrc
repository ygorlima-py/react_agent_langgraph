dockerremoveall() {
  # para e remove todos os containers
  docker stop $(docker ps -aq) 2>/dev/null || true
  docker rm   $(docker ps -aq) 2>/dev/null || true

  # remove imagens
  docker rmi  $(docker images -aq) 2>/dev/null || true

  # remove volumes
  docker volume rm $(docker volume ls -q) 2>/dev/null || true
}
