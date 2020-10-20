## Generating password:
```
python -c 'import random; result = "".join([random.choice("abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)") for i in range(50)]); print(result)'
```

## Restarting celery
sudo supervisorctl restart abroadin_celery_beat && sudo supervisorctl restart abroadin_celery_worker