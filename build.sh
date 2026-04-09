#!/usr/bin/env bash
set -e

pip install -r requirements.txt

git clone https://github.com/ai-dynamo/aiconfigurator.git

cd aiconfigurator

# Skip LFS → use pointer files (works for our use-case)
cd ..

pip install -e ./aiconfigurator


