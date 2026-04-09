#!/usr/bin/env bash
set -e

pip install -r requirements.txt

if [ ! -d "aiconfigurator" ]; then
  git clone https://github.com/ai-dynamo/aiconfigurator.git
fi

cd aiconfigurator
git lfs install
git lfs pull
cd ..

pip install -e ./aiconfigurator
