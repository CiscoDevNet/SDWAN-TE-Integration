# Cisco SD-WAN and ThousandEyes Integration

# Objective 

*   How to use ThousandEyes Webhook Notifications and vManage APIs to automate central policy activation based on Webhook Notifications for alerts from ThousandEyes.

# Requirements

To use this code you will need:

* Python 3.7+
* vManage user login details. (User should have privilege level to activate central policies)

# Install and Setup

- Clone the code to local machine.

```
git clone https://github.com/suchandanreddy/SDWAN-TE-Integration
cd SDWAN-TE-Integration
```
- Setup Python Virtual Environment (requires Python 3.7+)

```
python3.7 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

- Create **config_details.yaml** using below sample format to provide the login details of vManage.

## Example:

```
# vManage Connectivity Info

vmanage_host: 
vmanage_port: 
vmanage_username:
vmanage_password:
```

- Run the script using the command `python3 sdwan-te-integration.py` and once Webhook Server recieves alert from the Thousands it triggers API call to vManage to activate the Central Policy with name `Global-Policy-v4`

## Example:

```
$ python3 sdwan-te-integration.py
 * Serving Flask app "sdwan-te-integration" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5500/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 119-530-476
Activating Central Policy Global-Policy-v4
52.52.36.83 --- [16/Feb/2021 18:34:43] *POST /policy_activate HTTP/1.1* 200 -

```