from irods.column import Like
from irods.models import Collection, DataObject
from datetime import datetime
from setup_session import setup_session
from logger import logger
import re

def handle_exception():
    raise SystemExit(0)


class IrodsData():
    def __init__(self):
        self.session = None
        self.data = {'collections': {}, 'groups': []}
        self.logger=logger

    def collect(self):
        self.data['collections'] = self.get_home_collections()
        self.data['groups'] = self.get_groups()

        group_members = []
        for g in self.data['groups']:
            group_members = list(set(group_members + self.data['groups'][g]['members']))
            group_members = list(set(group_members + self.data['groups'][g]['read_members']))
        return self.data

    def close_session(self):
        self.session.cleanup()
        self.session = None
        self.logger.info('irods session closed')

    def get_session(self):
        try:
            self.logger.info('setup irods session')
            self.session = setup_session()
            self.get_home_collections()  # try once to see if we are logged in
        except:
            self.logger.error('could not get collections and groups, probably an authentication error')
            handle_exception()
        return True

    def get_home_collections(self):
        collections = {}
        coll = self.session.collections.get(f'/{self.session.zone}/home')
        for col in coll.subcollections:
            collections[col.name] = {}
        return collections


    def get_member_count(self, group_name):
        internal = 0
        external = 0
        for user in self.session.user_groups.get(group_name).members:
            if user.name.endswith(("vu.nl", "acta.nl")):
                internal += 1
            else:
                external += 1
        return internal, external

    def get_groups(self):
        groups = {}
        for path in self.data['collections']:
            if path.startswith('research-') or path.startswith('datamanager-'):
                groupname = path
                groups[groupname] = {}
                group_obj = self.session.user_groups.get(groupname)
                groups[groupname]['category'] = group_obj.metadata.get_one('category').value
                try:
                    groups[groupname]['data_classification'] = group_obj.metadata.get_one('data_classification').value
                except:
                    groups[groupname]['data_classification'] = "NA"
                member_names = [user.name for user in group_obj.members]
                groups[groupname]['members'] = member_names
                groups[groupname]['read_members'] = []
                if path.startswith('research-'):
                    read_group_obj = self.session.user_groups.get(groupname.replace('research-', 'read-', 1))
                    read_member_names = [user.name for user in read_group_obj.members]
                    groups[groupname]['read_members'] = read_member_names
        return groups

