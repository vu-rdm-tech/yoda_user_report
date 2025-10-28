from setup_session import setup_session

from irodsdata import IrodsData
import os
from datetime import datetime

import json
from logger import logger


def collect(active, cutoff):
    """
    Collect all data from irods and return as a dict
    
    - login to irods
    - get all collections in home directory
    - get all groups
    - close irods session
    
    :return: a dict with all data
    """
    irodsdata = IrodsData()
    irodsdata.get_session()
    logger.info("start data collection")
    data = irodsdata.collect(active, cutoff)
    irodsdata.close_session()
    return data


def report(data, reportfile, active, cutoff):
    """
    Create a list of unique group members
    """
   
    report_data = []
    for group in data["groups"]:
        cat = data["groups"][group]["category"]
        members = data["groups"][group]["members"]
        for member in members:
            if member not in report_data:
                report_data.append(member)

    with open(reportfile, "w") as f:
        f.write("Yoda users report.\n")
        if active:
            f.write(f"Users in groups with newest file less than {cutoff} days old AND no files + group created less than {cutoff} days ago\n OR in a datamanger group.\n")
        f.write(f"Generated {datetime.now().strftime('%Y%m%d at %H:%M:%S')}.\n\n")
        for member in report_data:
            f.write(f"{member}\n")

    logger.info(f"Report file written to {reportfile}")
    logger.info("script finished")


def main():
    logger.info(f"start script {os.path.realpath(__file__)}")
    active=True
    cutoff=6*365/12
    data = collect(active=active, cutoff=cutoff)
    report(data, f"./data/yoda_users-{datetime.now().strftime('%Y%m%d')}.csv", active=active, cutoff=cutoff)



if __name__ == "__main__":
    main()
