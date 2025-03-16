all:
	@docker compose up --build -d
	
	@echo "FTP Server IP:"
	@docker inspect ftp_server | grep "IPAddress"
	@echo "FTP Server MAC:"
	@docker inspect ftp_server | grep "MacAddress"

	@echo "FTP Client IP:"
	@docker inspect ftp_client | grep "IPAddress"
	@echo "FTP Client MAC:"
	@docker inspect ftp_client | grep "MacAddress"

	@echo "Attacker IP:"
	@docker inspect attacker | grep "IPAddress"
	@echo "Attacker MAC:"
	@docker inspect attacker | grep "MacAddress"

clean:
	@docker ps -aq | xargs docker rm -f

re: clean all
