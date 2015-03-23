#!/bin/bash

# Make sure only root can run our script
if [[ $EUID -eq 0 ]]; then
   echo "User installation requires not-root user. Use 'sudo make install' for not-root setup" 1>&2
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

LOG_DIR="${DIR}/tmp"
LOG_DIR_SED=$(echo $LOG_DIR | sed -e 's/[]/()$*.^|[]/\\&/g')
DIR_SED=$(echo $DIR | sed -e 's/[]/()$*.^|[]/\\&/g')
PYTHON_PATH=$(which python)
PYTHON_SED=$(echo ${PYTHON_PATH} | sed -e 's/[]/()$*.^|[]/\\&/g')
PATH_DIR_JSON="$DIR/directory.json"

mkdir -p "${DIR}/tmp" 2>&1

# Create files
cp "$DIR/directory.linux.json" "${PATH_DIR_JSON}"

# Substitute alias with script directory
#ln -s "${DIR}/application" "${SYMLINK}"
sed -i "s/LOG_DIR/${LOG_DIR_SED}/g" "${PATH_DIR_JSON}"
sed -i "s/SCRIPT_DIR/${DIR_SED}/g" "${PATH_DIR_JSON}"
sed -i "s/PYTHON_PATH/${PYTHON_SED}/g" "${PATH_DIR_JSON}"

# Python libraries installation
pip install --user -q tvdb_api transmissionrpc 2>&1
echo "Install completed"
