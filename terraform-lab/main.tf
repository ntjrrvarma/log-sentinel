terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}

# 1. Download Image (Equivalent to 'docker pull')
resource "docker_image" "nginx" {
  name         = "nginx:latest"
  keep_locally = false
}

# 2. Run Container (Equivalent to 'docker run -d -p 8080:80')
resource "docker_container" "nginx" {
  image = docker_image.nginx.image_id
  name  = "tutorial_server"

  ports {
    internal = 80
    external = 8080
  }
}