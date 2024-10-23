from irods.column import Like
from irods.models import Collection, DataObject
from datetime import datetime
from setup_session import setup_session
from logger import logger
import re


def handle_exception():
    raise SystemExit(0)


class IrodsData:
    def __init__(self):
        self.session = None
        self.data = {"collections": {}, "groups": []}
        self.logger = logger

    def collect(self):
        """
        Collects all data from irods
        
        - login to irods
        - get all collections in home directory
        - get all groups
        - close irods session
        
        :return: a dict with all data
        """
        self.data["collections"] = self.get_home_collections()
        self.data["groups"] = self.get_groups()

        group_members = []
        for g in self.data["groups"]:
            group_members = list(set(group_members + self.data["groups"][g]["members"]))
            group_members = list(
                set(group_members + self.data["groups"][g]["read_members"])
            )
        return self.data

    def close_session(self):
        """
        Close the irods session
        
        - cleanup the session
        - set self.session to None
        - log the action
        """
        self.session.cleanup()
        self.session = None
        self.logger.info("irods session closed")

    def get_session(self):
        """
        Establishes a session with the iRODS server.

        - Logs the session setup process.
        - Attempts to set up the session and verify login by accessing home collections.
        - Logs and handles exceptions if authentication fails.

        :return: True if session setup is successful, otherwise terminates the program.
        """
        try:
            self.logger.info("setup irods session")
            self.session = setup_session()
            self.get_home_collections()  # try once to see if we are logged in
        except:
            self.logger.error(
                "could not get collections and groups, probably an authentication error"
            )
            handle_exception()
        return True

    def get_home_collections(self):
        """
        Get all collections in home directory
        
        - get all subcollections from home directory
        - return a dict with all collection names as keys
        
        :return: a dict with all home collections
        """
        collections = {}
        coll = self.session.collections.get(f"/{self.session.zone}/home")
        for col in coll.subcollections:
            collections[col.name] = {}
        return collections

    def get_member_count(self, group_name):
        """
        Count the number of members in a group that are internal or external to the VU.
        
        :param group_name: The name of the group to count members for
        :return: a tuple of two integers, the first is the number of internal members, the second the number of external members
        """
        internal = 0
        external = 0
        for user in self.session.user_groups.get(group_name).members:
            if user.name.endswith(("vu.nl", "acta.nl")):
                internal += 1
            else:
                external += 1
        return internal, external

    def get_groups(self):
        """
        Retrieve information about groups from iRODS sessions.
        
        Iterates through the collections data and extracts group information based on the fact the path name equals the group name.
        
        :return: a dictionary containing group information
        """
        groups = {}
        for path in self.data["collections"]:
            if path.startswith("research-") or path.startswith("datamanager-"):
                groupname = path
                groups[groupname] = {}
                group_obj = self.session.user_groups.get(groupname)
                groups[groupname]["category"] = group_obj.metadata.get_one(
                    "category"
                ).value
                try:
                    groups[groupname]["data_classification"] = (
                        group_obj.metadata.get_one("data_classification").value
                    )
                except:
                    groups[groupname]["data_classification"] = "NA"
                member_names = [user.name for user in group_obj.members]
                groups[groupname]["members"] = member_names
                groups[groupname]["read_members"] = []
                if path.startswith("research-"):
                    read_group_obj = self.session.user_groups.get(
                        groupname.replace("research-", "read-", 1)
                    )
                    read_member_names = [user.name for user in read_group_obj.members]
                    groups[groupname]["read_members"] = read_member_names
        return groups
