#! /bin/bash

echo ":: Generating file list ::"
find . | grep -v ".git" | egrep "\.(pl|py|js|html|go)$"



