#! /bin/bash

echo ":: File List ::"
find . | grep -v ".git" | egrep "\.(pl|py|js)$"

