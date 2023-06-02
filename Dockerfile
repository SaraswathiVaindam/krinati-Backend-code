version: "3"
services:
  app:
    build: .
    environment:
      - CACHE_REDIS_URL=redis://localhost:5000/1
    ports:
      - 5000:5000
    depends_on:
      - redis
  redis:
    image: redis:latest

