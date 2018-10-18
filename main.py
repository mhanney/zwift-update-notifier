from __future__ import print_function
import sys
import io
import os
import os.path
import logging
import platform
import json
import xml.etree.ElementTree as ET

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# figure out path to where this script is running so that imports are relative
current_dir = os.path.dirname(os.path.realpath(__file__))

root_dir = current_dir if "LAMBDA_TASK_ROOT" not in os.environ else os.environ[
    "LAMBDA_TASK_ROOT"]

# to support local development on windows, or macos, or linux
# Resut is Windows, Linux, MacOS
current_platform = platform.system()

# On linux, put python modules and any .so files in lib.
# It must be called lib and in the same level as the handler
# because lib is in the LD_LIBRARY_PATH for C shared object linking.
platform_lib = "winlib" if current_platform == "Windows" else "lib"

# add the local lib dir to the search path for imports
libs = os.path.join(root_dir, platform_lib)

log = print if current_platform == "Windows" else logger.info

tmp_dir = os.path.join(root_dir,
                       "tmp") if current_platform == "Windows" else "/tmp"

if not os.path.exists(tmp_dir):
  os.makedirs(tmp_dir)

ZWIFT_CUR_VER_FILE = "Zwift_ver_cur.xml"
ZWIFT_CUR_VER_URL = "https://cdn.zwift.com/gameassets/Zwift_Updates_Root/{}".format(
    ZWIFT_CUR_VER_FILE)

log('libs: {}'.format(libs))

sys.path.insert(0, libs)

import requests
import boto3
snsClient = boto3.client('sns')


def get_latest_zwift_manifest():
  cur_ver_file = requests.get(ZWIFT_CUR_VER_URL)
  ver = ET.fromstring(cur_ver_file.content)
  return ver.get('manifest')


def handler(event, context):
  old_version = "Zwift_1.0.30589_manifest.xml"
  log("Downloading manifest..")
  latest_version = get_latest_zwift_manifest()

  is_new = False if latest_version == old_version else True

  log("Is new: {}".format(is_new))

  if (is_new):
    log("Old version: {}".format(old_version))
    log("New version: {}".format(latest_version))
    message = {'latest': latest_version, 'previous': old_version}

    try:
      snsClient.publish(
          TopicArn=os.environ["SNS_TOPIC_ARN"],
          Message=json.dumps({
              'default': json.dumps(message)
          }),
          MessageStructure='json')
    except:
      log("Error publishing sns: {}".format(sys.exc_info()[0]))


# for testing locally
if __name__ == '__main__':
  handler(None, None)