TvShowWatch
===========

Another TV Show download scheduler via Torrent.

## Description

You regulary miss your favorite TV show broadcast? TvShowWatch take care of everything for you!
Like [SickBeard][4], TSW use [TheTvDb][5] database to know when your favorite TV shows are broadcasted. Once available on your torrent tracker, TSW pushes it to Transmission server and, potentially, transfer files to a local directory.

## What is needed?
+ ```Transmission client```[8]. You can use [SynoCommunity][16] synology package. In this case default configuration of TSW will be:
 + server: localhost
 + port: 9091
 + user and password chosen during transmission installation
+ (facultative) ```T411 account```[6]
+ (facultative) ```A seedbox``` with transmission client & FTP access (user/password must be identical)

## What service are used
+ TV Show planning: [TheTvDb][5] (no plan to use another one for moment).
+ Torrent search providers: [T411][6] or [KickAss][14] (other providers are welcome, all I need is an easy JSON API).
+ Torrent manager: [Transmission][7] (no plan to use another one for moment).
+ Transfer protocol: FTP (plan to propose Rsync transfer [#6][9])
+ Javascript Libraries: Jquery [11] and JQGrid [12]
+ Web UI Framework: JqueryUI [13] (thinking about [Webix][17])

## Install notice

### Python standalone

Here are the dependencies:
+ ***python*** - The following libraries will be automatically installed
+ ```tvdb_api``` ([here][1])
+ ```requests``` (see [this repo][2])
+ ```transmissionrpc``` (see [this repo][3])
+ ```cherrypy``` (see [website] [10])
+ ```python-crontab``` (see [website] [15])

#### Linux setup
Installation will schedule hourly torrent tracking and launch web interface.

Execute ```make install``` in the installation directory.

Then execute ```script/start-stop-status start```

Go to ```http://127.0.0.1:1204``` for web interface

For CLI usage (facultative):
+ use ```./tvShowWatch --init``` to create configuration file -or- go to web interface ```http://localhost/tvshowwatch/```
+ Use ```./tvShowWatch -h``` for command line usage

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
[14]: http://kickass.to
[15]: https://pypi.python.org/pypi/python-crontab
[16]: https://synocommunity.com/
[17]: http://webix.com/
