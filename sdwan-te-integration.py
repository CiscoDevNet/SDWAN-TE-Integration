import requests
import sys
import json
import os
import logging
import yaml
from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from vmanage.api.authentication import Authentication
from vmanage.api.central_policy import CentralPolicy
from vmanage.api.utilities import Utilities
from logging.handlers import TimedRotatingFileHandler
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings()

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'sdwandemo'
app.config['BASIC_AUTH_PASSWORD'] = 'sdwandemo-TE12!'

basic_auth = BasicAuth(app)

def get_logger(logfile, level):
    '''
    Create a logger
    '''
    if logfile is not None:

        '''
        Create the log directory if it doesn't exist
        '''

        fldr = os.path.dirname(logfile)
        if not os.path.exists(fldr):
            os.makedirs(fldr)

        logger = logging.getLogger()
        logger.setLevel(level)

        log_format = '%(asctime)s | %(levelname)-8s | %(funcName)-20s | %(lineno)-3d | %(message)s'
        formatter = logging.Formatter(log_format)

        file_handler = TimedRotatingFileHandler(logfile, when='midnight', backupCount=7)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        logger.addHandler(file_handler)

        return logger

    return None

@app.route('/policy_activate',methods=['POST'])
@basic_auth.required
def policy_activation():
    try:

        log_level = logging.DEBUG
        logger = get_logger("log/sdwan-te-integration.txt", log_level)

        if logger is not None:
            logger.info("Loading vManage login details from YAML\n")

        data = json.loads(request.data)

        with open("config_details.yaml") as f:
            config = yaml.safe_load(f.read())

        vmanage_host = config["vmanage_host"]
        vmanage_port = config["vmanage_port"]
        username = config["vmanage_username"]
        password = config["vmanage_password"]

        session = Authentication(host=vmanage_host, port=vmanage_port, user=username, password=password).login()

        name = "Global-Policy-v4"

        vmanage_central_policy = CentralPolicy(session, vmanage_host, vmanage_port)
        central_policy_dict = vmanage_central_policy.get_central_policy_dict(remove_key=True)
        if name in central_policy_dict:
            print(f'Activating Central Policy {name}')
            action_id = vmanage_central_policy.activate_central_policy(name, central_policy_dict[name]['policyId'])
            utils = Utilities(session, vmanage_host, vmanage_port)
            utils.waitfor_action_completion(action_id)
        else:
            return jsonify(f'Cannot find Central Policy {name}'), 200

    except Exception as exc:
        print('Exception line number: {}'.format(sys.exc_info()[-1].tb_lineno), type(exc).__name__, exc)
        return jsonify(str(exc)), 500

    return jsonify(f'Activated Policy {name}'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)