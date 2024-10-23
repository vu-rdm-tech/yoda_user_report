from setup_session import setup_session

from irodsdata import IrodsData
import os
from datetime import datetime

import json
from logger import logger


def collect():
    irodsdata = IrodsData()
    irodsdata.get_session()
    logger.info('start data collection')
    data=irodsdata.collect()
    irodsdata.close_session()
    return data


def report(data, reportfile):

    # report

    report_data={}

    for group in data['groups']:

        cat = data['groups'][group]['category']

        members = data['groups'][group]['members']

        if cat not in report_data:

            report_data[cat]={

                'datamanagers': [],

                'research-groups': []

            }

        if group.startswith('datamanager-'):

            report_data[cat]['datamanagers']=members

        elif group.startswith('research-'):

            report_data[cat]['research-groups'].append(group)


    with open(reportfile, 'w') as f:
        f.write("Yoda datamanager report\n")
        f.write(f"Generated {datetime.now().strftime('%Y%m%d at %H:%M:%S')}\n\n")
        for cat in dict(sorted(report_data.items())):

            f.write(f'{cat}\n')

            f.write('\tdatamanagers:\n')

            for d in report_data[cat]['datamanagers']:

                f.write(f'\t\t{d}\n')

            f.write('\tresearch collections:\n')

            for g in report_data[cat]['research-groups']:

                f.write(f'\t\t{g}\n')
            f.write('\n')

    logger.info(f"Report file written to {reportfile}")


    logger.info('script finished')


def main():
    logger.info(f'start script {os.path.realpath(__file__)}')
    data=collect()
    report(data,f"./data/yoda_datamanagers-{datetime.now().strftime('%Y%m%d')}.txt")


if __name__ == "__main__":
    main()