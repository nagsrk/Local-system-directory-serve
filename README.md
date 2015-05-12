# Local-system-directory-serve
This is a webApp for local system directory mapping to each authenticated user

This App can be used as it is by adding the required .html in /templates directory. 
Currently it will authenticate users and authorize access to local system directories. 
So, for example if you are to serve/distribute thousands of logs to users, 
simply filter the data and redirect the users to specific directory. 
So no hassles of maintaining a Database for randomly generated data like logs. Simply map the user to a directory.

The file at /Local-system-directory-serve/app/lib/EditRsyslog.py will filter and create directories based on the IP address of incoming logs and the 'App' uses the configuration file generated to serve based on the user and directory.
