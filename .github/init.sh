#!/usr/bin/env bash

repo_urlname=$(basename -s .git `git config --get remote.origin.url`)
repo_name=$(basename -s .git `git config --get remote.origin.url` | tr '-' '_' | tr '[:upper:]' '[:lower:]')
repo_owner=$(git config --get remote.origin.url | awk -F '/' '{print $4}')
echo "Repo name: ${repo_name}"
echo "Repo owner: ${repo_owner}"
echo "Repo urlname: ${repo_urlname}"

if [ -f ".github/workflows/rename_project.yml" ]; then
    .github/rename_project.sh -a "${repo_owner}" -n "${repo_name}" -u "${repo_urlname}" -d "Awesome ${repo_name} created by ${repo_owner}"
fi

echo "Done! review, commit and push the changes"