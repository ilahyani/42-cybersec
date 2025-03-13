all:
	@docker build -t onion-img .
	@docker run -d -v ~/.ssh/my_docker_key.pub:/root/.ssh/authorized_keys -p 8080:80 -p 2424:4242 -p 9050:9050 -p 9051:9051 --name onion onion-img
	@sleep 3 && docker exec -it onion cat /var/lib/tor/hidden_service/hostname

clean:
	@docker rm -f onion

re: clean all