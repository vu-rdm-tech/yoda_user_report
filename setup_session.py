#!/usr/bin/env python3
from getpass import getpass

import json
from irods.session import iRODSSession
from pathlib import Path
from getpass import getpass
from logger import logger
import ssl

def get_irods_environment(irods_environment_file):
    """Reads the irods_environment.json file, which contains the environment

    configuration."""

    logger.info(
        f"Trying to retrieve connection settings from: {irods_environment_file}"
    )

    with open(irods_environment_file, "r") as f:

        return json.load(f)


def setup_session(ca_file=None):
    """Use irods environment files to configure a iRODSSession. User is prompted for the password"""

    irods_env = get_irods_environment(f"{Path.home()}/.irods/irods_environment.json")

    logger.info(f"irods_enviroment.json found")

    logger.info(f"Trying to login to {irods_env['irods_host']}")

    password = getpass(f"Enter valid DAP for user {irods_env['irods_user_name']}: ")

    ssl_context = ssl.create_default_context(
        purpose=ssl.Purpose.SERVER_AUTH, cafile=ca_file, capath=None, cadata=None
    )

    ssl_context.check_hostname = False

    ssl_context.verify_mode = ssl.CERT_NONE

    ssl_settings = {
        "client_server_negotiation": "request_server_negotiation",
        "client_server_policy": "CS_NEG_REQUIRE",
        "encryption_algorithm": "AES-256-CBC",
        "encryption_key_size": 32,
        "encryption_num_hash_rounds": 16,
        "encryption_salt_size": 8,
        "ssl_context": ssl_context,
    }

    session = iRODSSession(
        host=irods_env["irods_host"],
        port=irods_env["irods_port"],
        user=irods_env["irods_user_name"],
        password=password,
        zone=irods_env["irods_zone_name"],
        authentication_scheme="pam",
        **ssl_settings,
    )

    return session
