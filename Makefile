EXEC=TvShowWatch.spk

syno: TvShowWatch.spk

TvShowWatch.spk: syno/package.tgz syno/INFO syno/scripts syno/PACKAGE_ICON.PNG
	cd syno && tar cvf $@ package.tgz INFO scripts PACKAGE_ICON.PNG
	mv syno/$@ .

syno/package.tar: syno/application LICENSE README.md
	tar cvf package.tar *.py LICENSE README.md
	mv package.tar syno
	cd syno && tar rvf package.tar application

syno/package.tgz: syno/package.tar
	gzip -c syno/package.tar > $@

clean:
	for i in `find . -name "*.pyc"`; do rm -rf $i ; done
	for i in `find . -name "*~"`; do rm -rf $i ; done
#	for i in `find . -name "*.xml"`; do rm -rf $i ; done

mrproper: clean
	rm -rf $(EXEC)
	rm -rf syno/package.tgz
