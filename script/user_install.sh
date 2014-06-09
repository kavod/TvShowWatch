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

LOG_DIR="${DIR}/etc"
LOG_DIR_SED=$(echo $LOG_DIR | sed -e 's/[]/()$*.^|[]/\\&/g')
DIR_SED=$(echo $DIR | sed -e 's/[]/()$*.^|[]/\\&/g')

SYMLINK="${HOME}/public_html/tvshowwatch"

if [ -h ${SYMLINK} ]
then
    echo "TvShowWatch is already installed on this box"
    exit 1
fi

touch ${LOG_DIR}/TSW.log.json
chmod 775 ${DIR}/application/tmp
APACHE_GROUP="$(grep APACHE_RUN_GROUP /etc/apache2/envvars|cut -d'=' -f2)"
chgrp ${APACHE_GROUP} ${DIR}/application/tmp

# Create files
cp -v "$DIR/directory.linux.json" "$DIR/directory.json"

# Substitute alias with script directory
ln -s "${DIR}/application" "${SYMLINK}"
sed -i "s/LOG_DIR/${LOG_DIR_SED}/g" "$DIR/directory.json"
sed -i "s/SCRIPT_DIR/${DIR_SED}/g" "$DIR/directory.json"

# Python libraries installation
#/usr/bin/env easy_install tvdb_api transmissionrpc requests
echo "User libraries cannot be install without root access. Please check following libraries are installed:"
echo "- tvdb_api"
echo "- transmissionrpc"
echo "- requests"
echo "Installation completed. Use http://localhost/~yourUser/tvshowwatch/ to manage TvShowWatch"
echo "Please note logfile is located in ${LOG_DIR}"
