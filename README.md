TvShowWatch
===========

Another TV Show download scheduler via Torrent.

## Description

You regulary miss your favorite TV show broadcast? TvShowWatch take care of everything for you!
Like [SickBeard][4], TSW use [TheTvDb][5] database to know when your favorite TV shows are broadcasted. Once available on your torrent tracker, TSW pushes it to Transmission server and, potentially, transfer files to a local directory.

## Compatibility
+TV Show planning: [TheTvDb][5] (no plan to use another one for moment).
+Torrent tracker: [T411][6] (facultative, Kickass torrent is planed for next release)
+Torrent manager: [Transmission][7] (no plan to use another one for moment).
+Transfer protocol: FTP (plan to propose Rsync transfer [#6][9])
+Javascript Libraries: Jquery [11] and JQGrid [12]
+Web UI Framework: JqueryUI [13]

## Install notice

### Python standalone

Here are the dependencies:
+ ***python*** - The following libraries will be automatically installed
+ ```tvdb_api``` - download and install from [here][1].
+ ```requests``` - run ```sudo pip install request```, see [this repo][2].
+ ```transmissionrpc``` - run ```sudo pip transmissionrpc```, see [this repo][3]
+ ```cherrypy``` - run ```sudo pip cherrypy```, [10]

#### Root setup
Install with root user allow job schedule for torrent tracking. Without it, you will have to manually push TvShowWatch every time.
Just launch ```make install``` in the installation directory.
Then use ```./tvShowWatch --init``` to create configuration file -or- go to web interface ```http://localhost/tvshowwatch/```
Use ```./tvShowWatch -h``` for command line usage

#### User setup
Note that user setup does not allow job schedule via crontab.
Just launch ```make user_install``` in the installation directory.
Then use ```./tvShowWatch --init``` to create configuration file -or- go to web interface ```http://localhost/~yourUser/tvshowwatch/```
Use ```./tvShowWatch -h``` for command line usage

### Synology Package

From source, just use the Makefile:
```
make mrproper
make syno
```
This will generate the package tvShowWatch.spk you can add in the Synology Packages Center.
Python dependant libraries will be automatically installed. Please note that each time Python package is updated, additionnal libraries are removed. You will have to manually reinstall them -or- reinstall TvShowWatch package.
Please note the "run" status significates web server is run and automatic seek is scheduled (every 1 hour).

[1]: https://github.com/dbr/tvdb_api
[2]: https://github.com/kennethreitz/requests
[3]: http://pythonhosted.org/transmissionrpc/
[4]: http://http://sickbeard.com/
[5]: http://thetvdb.com/
[6]: http://t411.me
[7]: https://github.com/kavod/TvShowWatch/issues/7
[8]: http://www.transmissionbt.com/
[9]: https://github.com/kavod/TvShowWatch/issues/6
[10]: http://www.cherrypy.org/
[11]: https://jquery.com/
[12]: http://www.trirand.com/blog/
[13]: http://jqueryui.com/
