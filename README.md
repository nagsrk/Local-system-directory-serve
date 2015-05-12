# Local-system-directory-serve
This is a webApp for local system directory mapping to each authenticated user

This App can be used as it is by adding the required .html in /templates directory. 
Currently it will authenticate users and authorize access to local system directories. 
So, for example if you are to serve/distribute thousands of logs to users, 
simply filter the data and redirect the users to specific directory. 
So no hassles of maintaining a Database for randomly generated data like logs. Simply map the user to a directory.

The file at /Local-system-directory-serve/app/lib/EditRsyslog.py filters the incoming logs and creates directories based on the IP address. The files in the 'App' directory uses the configuration file generated to serve user files based on the user and directory after authentication.
