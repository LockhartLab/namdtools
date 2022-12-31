
# meant to be run in root directory

read major minor patch <<< $(bash .scripts/get_version.sh)
patch=$(expr $patch + 1)
git tag ${major}.${minor}.${patch}


