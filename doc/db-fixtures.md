Create fixtures:
================
- python manage.py dumpdata > fixtures/fixtures.json

Applying fixtures:
==================
as> python manage.py migrate
as> python manage.py sqlflush > /tmp/flushdb.sql
as> psql -h 10.241.145.2 -U domino -f /tmp/flushdb.sql
as> python manage.py loaddata fixtures/fixtures.json
