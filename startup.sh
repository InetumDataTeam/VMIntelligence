#!/bin/bash

apt-get update
if ! command -v python3.9 &>/dev/null; then
  apt-get install python3.9 -y
  apt-get install python3-pip -y
fi
if ! command -v docker &>/dev/null; then
  apt-get install docker-ce docker-ce-cli containerd.io
fi

pip3 install --no-cache-dir -r requirements.txt
pip3 install --force-reinstall dist/VMIntelligence-1.0.1-py2.py3-none-any.whl

docker compose up &
# ici mettre les variables d'env

vmintelligence --pwd "$vmintel_pwd" --bdd_name "$vmintel_bdd_name" --login "$vmintel_login" --host "$vmintel_host" --port "$vmintel_port" --path "$vmintel_path"
