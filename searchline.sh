#! /bin/bash

echo ":: Generating file list ::"
echo ":: Start Search ::"

keyword="json"

for file in $(find ./templates | grep -v ".git" | egrep "\.(pl|py|js|html|go|rs|rb|cpp|h)$")
do
    trimmed_lines=()

    # Read the file line by line, trim whitespace, and store in the array
    while IFS= read -r line; do
        trimmed_line=$(echo "$line" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
        trimmed_lines+=("$trimmed_line")
    done < $file

    # Print the contents of the array
    for ((i = 0; i < ${#trimmed_lines[@]}; i++)); do
        if [[ ${trimmed_lines[i]} =~ $keyword ]]; then
            echo ":: [$file] :: $((i + 1)) :: ${trimmed_lines[i]}"
        fi
    done
done



