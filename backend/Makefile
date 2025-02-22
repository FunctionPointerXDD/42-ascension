all:
	mkdir -p ./nginx/cert
	docker compose up -d --build \
	&& docker compose logs -f --tail 50

clean:
	docker compose down -t 1 && docker compose rm

fclean:
	docker compose down -v -t 1 --rmi local
	docker system prune -af
	rm -f ./nginx/cert/*

re:
	make fclean && make all

.PHONY: all clean fclean re