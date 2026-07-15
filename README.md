# PC-information-to-HA
This script is designed to integrate your Ubuntu PC with Home Assistant. This script is better than the larger/other programs and scripts because it's very lightweight and doesn't run as a huge background process.

# Installation for any ubuntu/debian based pc:
First, install depencies:

sudo apt update
sudo apt install python3-full python3-venv

Next, create your virtual environment:
python3 -m venv ~/ha-monitor-env (or any name of your choice)
source ~/ha-monitor-env/bin/activate

Then install the python packages:
pip install requests psutil

Then clone this repo:

git clone https://github.com/joel2009gh/PC-information-to-HA
then cd into the folder, and edit the config.json (such as the name, your HA url, and LL-token)

How to make a Long-Lived Access Token...
Go to your portal, then click on your profile, then click on security and scroll down.
Then, make a systemd service.

Add:

(copy the .service file to your systemd folder, most likely its in /etc/systemd/system/
and change /your_username/ to your account's name

To continue, run these commands:

sudo systemctl daemon-reload
sudo systemctl enable ha-system-monitor
sudo systemctl start ha-system-monitor

This will enable the services.
Please verify that the service is running with: systemctl status ha-system-monitor

Now you will have HA entities running, as example:

sensor.my_linux_pc_cpu_usage
sensor.my_linux_pc_memory_usage
sensor.my_linux_pc_disk_usage
sensor.my_linux_pc_uptime
