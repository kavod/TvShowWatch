TvShowWatch
===========

Another TV Show download scheduler via Torrent.

### Description

You regulary miss your favorite TV show broadcast? TvShowWatch take care of everything for you!
Like [SickBeard][4], TSW use [TheTvDb][5] database to know when your favorite TV shows are broadcasted. Once available on your torrent tracker, TSW pushes it to Transmission server and, potentially, transfer files to a local directory.

### Compatibility
TV Show planning: [TheTvDb][5] (no plan to use another one for moment).
Torrent tracker: [T411][6] (plan to propose other trackers or public search engine, please suggest [#7][7])
Torrent manager: [Transmission][7] (no plan to use another one for moment).
Transfer protocol: FTP (plan to propose Rsync transfer [#6][9])


### Install notice

Here are the dependencies:

+ ```tvdb_api``` - download and install from [here][1].
+ ```requests``` - run ```sudo pip install request```, see [this repo][2].
+ ```transmissionrpc``` - run ```easy_install transmissionrpc```, see [this repo][3]

[1]: https://github.com/dbr/tvdb_api
[2]: https://github.com/kennethreitz/requests
[3]: http://pythonhosted.org/transmissionrpc/
[4]: http://http://sickbeard.com/
[5]: http://thetvdb.com/
[6]: http://t411.me
[7]: https://github.com/kavod/TvShowWatch/issues/7
[8]: http://www.transmissionbt.com/
[7]: https://github.com/kavod/TvShowWatch/issues/6
