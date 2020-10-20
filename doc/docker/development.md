1)
```
docker-compose -f docker-compose-develop.yml up -d && docker exec -u $UID -d abroadin_django_1 bash -c "python manage.py runserver 0.0.0.0:8000"
```
```
docker-compose -f docker-compose-develop.yml down
```

> For accessing shell:
```
docker exec -it -u $UID abroadin_django_1 bash
```
> For running in background:
```
docker exec -u $UID -d abroadin_django_1 bash -c "python manage.py runserver 0.0.0.0:8000"
```

> For monitoring Celery:
Run this in Django shell:
```
flower -A abroadin --port=5555
```
