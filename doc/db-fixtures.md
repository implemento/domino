Create fixtures:
================
- docker-compose exec as python manage.py dumpdata > app/fixtures/fixtures.json

Applying fixtures:
==================
as> python manage.py migrate
as> python manage.py sqlflush > /tmp/flushdb.sql
as> psql -h db -U domino -f /tmp/flushdb.sql
as> python manage.py loaddata fixtures/fixtures.json
