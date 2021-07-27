#!env python3.9
"""VEEAM AHV Proxy Dumper

This script creates a backup from VEEAM AHV Proxy configuration
and save them to local place.
In this way way you are able to periodically creates backup of your proxies.

Example:
     ./fetch.py --host myproxy.company.net:8100 --backup-password veeam

Authors:
    Martin Weber <martin.weber@de.clara.net>

Version: Version: 1.0.0
"""
import json
import re
import argparse
import time
import requests

PARSER = argparse.ArgumentParser(
            description="Create and Download AHV Config Backup")

PARSER.add_argument("--proxy-hostname",
                    type=str, required=True,
                    help="AHV Proxy Host")
PARSER.add_argument("--proxy-username",
                    type=str, required=False,
                    help="Proxy Username (default: %(default)s)",
                    default="veeam")
PARSER.add_argument("--proxy-password",
                    type=str, required=False,
                    help="Proxy Password (default: %(default)s)",
                    default="veeam")
PARSER.add_argument("--backup-password",
                    type=str, required=True,
                    help="Backup Password")
PARSER.add_argument("--backup-common",
                    action=argparse.BooleanOptionalAction,
                    help="Include Common Data",
                    default=True)
PARSER.add_argument("--backup-events",
                    action=argparse.BooleanOptionalAction,
                    help="Include Events Data",
                    default=False)
PARSER.add_argument("--out-dir",
                    type=str, help="Output directory (default: %(default)s)",
                    default="./")

ARGS = PARSER.parse_args()
print(ARGS)
class VeeamAhvAPIExeption(Exception):
    """Exception Wrapper for Veeam API Exceptions
    """

class VeeamAhvAPI():
    """Abstract VEEAM API Base class

    Should provide basic functionality like opening sessions etc.
    """
    __hostname = None
    __session_token = None

    def __init__(self, hostname):
        self.__hostname = hostname

    def session_token(self):
        """Returns the session token
        """
        return self.__session_token

    def ahv_proxy_url(self):
        """Return a normalized url for host arguments

        Will strip protocol at the beginning and
        check if port is set
        """
        host = str(self.__hostname)
        host = "https://" + host.replace(r'^https?://', '')
        if not re.search(r':\d+$', host):
            host = host + ":8100"

        return host

    def wait_for_task(self, task_id):
        """Wait for task if finishec

        Checks task status and wait a time to check again until the
        status is not running anymore.

        Returns:
          The response object result from the API

        Raises:
          VeeamAhvAPIExeption: if API status_code != 200
        """
        url = "{}/api/v1/Tasks/{}".format(self.ahv_proxy_url(), task_id)

        headers = {"Accept": "application/json",
                   "Authorization": self.session_token()}

        result = {"status": "running"}
        while result["status"].lower() == "running":
            time.sleep(1)

            res = requests.get(url, headers=headers, verify=False)
            if res.status_code != 200:
                raise VeeamAhvAPIExeption("Cannot create config")

            result = res.json()

        return result

    def open_session(self, username, password):
        """Call the API and opens a session

        Raises:
          VeeamAhvAPIExeption: if API status_code != 200
        """
        url = "{}/api/v1/Account/login".format(self.ahv_proxy_url())

        data = {"@odata.type":"LoginData",
                "Password": password,
                "Username": username}

        headers = {"Accept": "application/json",
                  "Content-Type": "application/json"}

        res = requests.post(url,
                            data=json.dumps(data),
                            headers=headers,
                            verify=False)

        if res.status_code != 200:
            raise VeeamAhvAPIExeption("Cannot login to AHV Proxy")

        self.__session_token = res.json()["token"]
        return True

class VeeamAhvAPIBackup(VeeamAhvAPI):
    """VEEAM Config Backup

    Provides funktionality to create Veeam backups
    """
    def start_create_config(self, backup_password, backup_common=True, backup_events=False):
        """Start create the configuration backup

        Creating the the Backup is asynchrounus.

        Returns:
          Task ID of the backup.

        Raises:
          VeeamAhvAPIExeption: if API status_code != 200
        """
        url = "{}/api/v1/saveconfig".format(self.ahv_proxy_url())

        data = {"isConfigNeed": backup_common,
                "isEventsNeed": backup_events,
                "password": backup_password,
                "@odata.type": "SaveConfig"}

        headers = {"Accept": "application/json",
                  "Content-Type": "application/json",
                  "Authorization": self.session_token()}

        res = requests.post(url,
                            data=json.dumps(data),
                            headers=headers,
                            verify=False)

        if res.status_code != 200:
            raise VeeamAhvAPIExeption("Cannot create config")

        return res.json()["asyncTaskId"]

    def download_config(self, task_result, destination):
        """Download the configuration backup

        Requires the last, successfull task result.
        Filename is fetch ftom the download string and
        save it to given out-dir directory

        """
        url = task_result["result"]["customResults"]["urlToFile"]
        filename = url.split("/").pop()
        filename = destination + "/" + filename

        headers = {"Authorization": self.session_token()}

        res = requests.get(url, headers=headers, verify=False)
        with open(filename, 'wb') as file:
            file.write(res.content)

def __main__():
    api = VeeamAhvAPIBackup(ARGS.proxy_hostname)

    try:
        if api.open_session(ARGS.proxy_username, ARGS.proxy_password):
            task_id = api.start_create_config(ARGS.backup_password,
                                              ARGS.backup_common,
                                              ARGS.backup_events)
            result = api.wait_for_task(task_id)
            api.download_config(result, ARGS.out_dir)
    except VeeamAhvAPIExeption as err:
        print(err)

__main__()
