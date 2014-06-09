#!/bin/bash

#....
# Make sure only root can run our script
if [[ $EUID -eq 0 ]]; then
   echo "This script must not be run as root" 1>&2
   exit 1
fi

# Get script directory
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$(dirname $( cd -P "$( dirname "$SOURCE" )" && pwd ))"
echo "Script directory: $DIR"
DIR_SED=$(echo $DIR | sed -e 's/[]/()$*.^|[]/\\&/g')

SYMLINK="${HOME}/public_html/tvshowwatch"

if [ ! -h ${SYMLINK} ]
then
    echo "TvShowWatch is not installed on this box for your user"
    exit 1
fi

# Remove site
rm "${SYMLINK}"
rm "${DIR}/directory.json"

