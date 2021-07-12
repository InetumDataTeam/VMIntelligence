#!/bin/bash

apt-get update
if ! command -v python3.9 &>/dev/null; then
  apt-get install python3.9 -y
  apt-get install python3-pip -y
fi
if ! command -v docker &>/dev/null; then
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
  apt-get install docker-ce docker-ce-cli containerd.io
fi

pip3 install --no-cache-dir -r requirements.txt
pip3 install --force-reinstall dist/VMIntelligence-1.0.2-py2.py3-none-any.whl

docker compose up -d

vmintelligence --pwd "$vmintel_pwd" --bdd_name "$vmintel_bdd_name" --login "$vmintel_login" --host "$vmintel_host" --port "$vmintel_port" --path "$vmintel_path"

# export vmintel_pwd=vmuser_1234 vmintel_bdd_name=vmintelligence vmintel_login=vm_user vmintel_host=localhost vmintel_port=5432 vmintel_path=/Users/camillesaury/Documents/workspace/python/VMIntelligence/res
