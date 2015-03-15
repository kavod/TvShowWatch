#!/bin/bash

#....
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
PATH_DIR_JSON="$DIR/application/api/directory.json"

# Get Apache conf directory
APACHE_DIR="$( apache2ctl -V|grep HTTPD_ROOT|cut -d'=' -f2|cut -d\" -f2 )"
echo "Apache conf directory: $APACHE_DIR"

FILE="${APACHE_DIR}/sites-available/tvshowwatch.conf"
FILE_ENABLE="${APACHE_DIR}/sites-enabled/tvshowwatch.conf"

if [ ! -f ${FILE_ENABLE} ]
then
    echo "TvShowWatch is not installed on this box"
    exit 1
fi

# Site unactivation
a2dissite tvshowwatch
service apache2 restart 

# Remove site
rm "${FILE}"
rm "${PATH_DIR_JSON}"

CRONFILE="/etc/cron.hourly/tvshowwatch"
if [ -f $CRONFILE ]; then
	rm $CRONFILE
else
	echo "TvShowWatch already unscheduled"
fi
