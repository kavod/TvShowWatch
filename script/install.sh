#!/bin/bash

LOG_DIR="/var/log"

# Make sure only root can run our script
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 1>&2
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
LOG_DIR_SED=$(echo $DIR | sed -e 's/[]/()$*.^|[]/\\&/g')
DIR_SED=$(echo $DIR | sed -e 's/[]/()$*.^|[]/\\&/g')

# Get Apache conf directory
APACHE_DIR="$( apache2ctl -V|grep HTTPD_ROOT|cut -d'=' -f2|cut -d\" -f2 )"
echo "Apache conf directory: $APACHE_DIR"

APACHE_USER="$(grep APACHE_RUN_USER /etc/apache2/envvars|cut -d'=' -f2)"
APACHE_GROUP="$(grep APACHE_RUN_GROUP /etc/apache2/envvars|cut -d'=' -f2)"

FILE="${APACHE_DIR}/sites-available/tvshowwatch"
FILE_ENABLE="${APACHE_DIR}/sites-enabled/tvshowwatch"

if [ -f ${FILE_ENABLE} ]
then
    echo "TvShowWatch is already installed on this box"
    exit 1
fi

touch ${LOG_DIR}/TSW.log.json
chown -R ${APACHE_USER}:${APACHE_GROUP} ${DIR}/etc
chown -R ${APACHE_USER}:${APACHE_GROUP} ${DIR}/application/tmp
chmod -R 775 ${DIR}/application/tmp

# Create files
cp -v "$DIR/script/tvshowwatch.conf" $FILE
cp -v "$DIR/directory.linux.json" "$DIR/directory.json"

# Substitute alias with script directory
sed -i "s/TSW_DIR/${DIR_SED}\/application\//g" $FILE
sed -i "s/LOG_DIR/${LOG_DIR_SED}/g" "$DIR/directory.json"
sed -i "s/SCRIPT_DIR/${DIR_SED}/g" "$DIR/directory.json"

# Python libraries installation
/usr/bin/env easy_install tvdb_api transmissionrpc requests

# Site activation
a2ensite tvshowwatch
service apache2 restart 

#ValidateConfFile() {
#	
#}
