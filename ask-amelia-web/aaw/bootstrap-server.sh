# vim .ssh/codecommit_rsa.pub
# vim .ssh/codecommit_rsa
# vim .ssh/config
# chmod 600 ../.ssh/config
# chmod 600 ../.ssh/config

#/bin/bash
sudo apt update
sudo apt upgrade -y
sudo reboot
sudo apt update
sudo apt upgrade -y
sudo apt install python3 -y
sudo apt install python3-pip -y
sudo python3 -m pip install --upgrade pip
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev python3-venv awscli
cd ~
mkdir askamelia
cd askamelia
https://github.com/bdsys/askamelia.git
cd ~/askamelia/ask-amelia-web/aaw
source bin/activate
pip3 install -r requirements.txt
# bashrc is required for persistant env vars for ssm-user an non-interactive use
echo "#Flask app env vars" >> ~/.bashrc
echo "export FLASK_APP=project" >> ~/.bashrc
echo "export FLASK_DEBUG=1" >> ~/.bashrc
echo "export FLASK_SECRET=$(echo $RANDOM | md5sum | head -c 32; echo)" >> ~/.bashrc
echo "export FLASK_AAW_USER_EMAIL=ameliadev@bdsys.net" >> ~/.bashrc
echo "export FLASK_AAW_USER_PASSWORD=timber" >> ~/.bashrc
echo "export FLASK_AAW_ACCESS_CODE_1=timber" >> ~/.bashrc
echo "export AA_API_GET_DB_ITEMS_BY_PK_URL=https://60w6yys7xj.execute-api.us-west-2.amazonaws.com/prod" >> ~/.bashrc
echo "export AA_API_UPDATE_DDB_ITEM_BY_PK_URL=https://culn41pxyc.execute-api.us-west-2.amazonaws.com/prod" >> ~/.bashrc
echo "export AA_API_GET_DB_ITEMS_URL=https://b4ljiw6wf4.execute-api.us-west-2.amazonaws.com/prod" >> ~/.bashrc
cd ~/askamelia/ask-amelia-web/aaw
python3 init_db.py
nohup flask run --host=0.0.0.0 --port=5000 &
