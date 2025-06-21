
# meant to be run from root dir

version=$(python -c "import versioneer; print(' '.join(versioneer.get_version().split('.')[:3]))")
echo $version
