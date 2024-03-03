# fraud-detection

https://hackernoon.com/setting-up-kafka-on-docker-for-local-development



```
docker volume rm fraud-detection_postgresql-volume

docker-compose down

docker-compose up -d
```


```
    DELETE FROM public.transactions;
    DELETE FROM public.fraudulent_analysis;
```
    