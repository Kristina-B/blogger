1. Setup virtualenv

$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

2. Setup database

$ sudo -u postgres psql
>> CREATE USER blogger WITH LOGIN PASSWORD '<password>';
>> CREATE DATABASE blogger OWNER blogger;

3. Recreate database

$ python scripts/initdb.py

4. Run debug server

$ python start_server.py
