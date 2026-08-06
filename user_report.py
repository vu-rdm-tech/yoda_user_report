from setup_session import setup_session

from irodsdata import IrodsData
import os
from datetime import datetime
import json
from logger import logger

import argparse

parser = argparse.ArgumentParser("user_report")
parser.add_argument('--active', action=argparse.BooleanOptionalAction)

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


def get_faculty(group_name):
    """
    Extract the faculty from a group name, e.g. "research-fsw-dep-project" -> "fsw"
    """
    parts = group_name.split("-")
    return parts[1] if len(parts) > 1 else ""


def report(data, reportfile, active, cutoff):
    """
    Create a list of unique group members
    """

    report_data = {}
    for group in data["groups"]:
        cat = data["groups"][group]["category"]
        faculty = get_faculty(group)
        members = data["groups"][group]["members"]
        for member in members:
            report_data.setdefault(member, set()).add(faculty)

    with open(reportfile, "w") as f:
        f.write("Yoda users report.\n")
        f.write(f"Generated {datetime.now().strftime('%Y%m%d at %H:%M:%S')}.\n\n")
        if active:
            f.write(f"Users in groups with newest file less than {cutoff} days old AND no files + group created less than {cutoff} days ago\n OR in a datamanager group.\n")
        for member, faculties in report_data.items():
            f.write(f"{member},{';'.join(sorted(faculties))}\n")

    logger.info(f"Report file written to {reportfile}")
    logger.info("script finished")


def main():
    logger.info(f"start script {os.path.realpath(__file__)}")
    cutoff=365/2
    args=parser.parse_args()
    active=args.active
    if active:
        logger.info(f"Users in groups with newest file less than {cutoff} days old AND no files + group created less than {cutoff} days ago\n OR in a datamanager group.\n")
    else:
        logger.info(f"Retrieving all users from all groups")
    data = collect(active=active, cutoff=cutoff)
    reportfilename=f"./data/yoda_users-{datetime.now().strftime('%Y%m%d')}.csv"
    logger.info(f"Write to {reportfilename}")
    report(data, reportfilename, active=active, cutoff=cutoff)



if __name__ == "__main__":
    main()
