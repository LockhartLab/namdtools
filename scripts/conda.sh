# Builds and uploads the conda package for the version pypi.sh just
# published, to the lockhartlab org on anaconda.org. Must run AFTER
# pypi.sh, since it reads the sdist checksum back from PyPI's JSON API
# (retrying briefly -- new uploads take a few seconds to index).
#
# Requires a local micromamba env named "namdtools-build" with conda-build
# and anaconda-client installed, and an active `anaconda login --at
# anaconda.org` session for an account with upload rights to lockhartlab:
#   micromamba create -n namdtools-build -c conda-forge conda-build anaconda-client
#   micromamba run -n namdtools-build anaconda login --at anaconda.org

version=$(git describe --tags --abbrev=0)

sha256=""
for i in 1 2 3 4 5
do
  sha256=$(curl -s "https://pypi.org/pypi/namdtools/$version/json" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    for f in d['urls']:
        if f['filename'].endswith('.tar.gz'):
            print(f['digests']['sha256'])
            break
except Exception:
    pass
")
  if [ -n "$sha256" ]
  then
    break
  fi
  sleep 5
done

if [ -z "$sha256" ]
then
  echo "could not fetch sdist sha256 from PyPI for $version yet, skipping conda build -- rerun scripts/conda.sh once PyPI has indexed the release"
  return
fi

sed -i '' -E "s/\{% set version = \"[^\"]+\" %\}/{% set version = \"$version\" %}/" conda-recipe/meta.yaml
sed -i '' -E "s/sha256: .+/sha256: $sha256/" conda-recipe/meta.yaml

rm -rf /tmp/conda-build-out
micromamba run -n namdtools-build conda-build conda-recipe -c conda-forge -c lockhartlab --output-folder /tmp/conda-build-out
micromamba run -n namdtools-build anaconda upload "/tmp/conda-build-out/noarch/namdtools-$version-py_0.conda" --user lockhartlab

git add conda-recipe/meta.yaml
git commit -m "conda-recipe: bump to $version"
git push origin main
