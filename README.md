docker load < Carolin_Hertel_bento_image.tar
docker run -d -p 3000:3000 admission_service:1.0.0
docker exec -it <your_docker_id> /bin/bash 
pytest src/tests/test_api.py -v