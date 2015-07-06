# Branch defunct, see altdates_merge

respa – Resource reservation and management service
===================

Installation
------------

1. Create the database.

```shell
sudo -u postgres createuser -L -R -S respa
sudo -u postgres psql respa
  CREATE EXTENSION postgis;
```
