Uses irods to create a simple list of Yoda categories, datamanagers and research groups.

To run you need to `pip install python-irodsclient`.

Make sure you have a valid `irods_environment.json` (see https://yoda.vu.nl/site/getting-started/icommands.html). Will work as well on Windows if you store the file in your profile `c:\Users\<username>\.irods\irod_environment.json` (see https://portal.yoda.vu.nl/user/data_transfer). 

- To generate the datamanager report run: `python datamanager_report.py`, a text file will be created in the 'data' directory. 
This script generates a list stating the datamanagers and group names per category.

- To generate the user report run: `python datamanager_report.py`, a csv file will be created in the 'data' directory. This is a flat list containing the usernames.

By default the script will filter "active" users:
- Members of groups that have a newest file newer than `cutoff` days go.
- Members of groups with an empty `research-` folder created after `cutoff` days ago.
- Members of datamanager groups

Set `active=False` in `user_report.py` `main()` to retrieve all irods users who are part of a group.

Note that irods does not store the last login date in its database, so this is the only reasonable method to retrieve users active in the past half year.

The script will prompt you for a Data Access Password.