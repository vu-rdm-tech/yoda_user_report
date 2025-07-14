Uses irods to create a simple list of Yoda categories, datamanagers and research groups.

To run you need to `pip install python-irodsclient`.

Make sure you have a valid `irods_environment.json` (see https://yoda.vu.nl/site/getting-started/icommands.html). Will work as well on Windows if you store the file in your profile `c:\Users\<username>\.irods\irod_environment.json`.

- To generate the datamanager report run: `python datamanager_report.py`, a text file will be created in the 'data' directory.

- To generate the user report run: `python datamanager_report.py`, a csv file will be created in the 'data' directory.


The script will prompt you for a Data Access Password.