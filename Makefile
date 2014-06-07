EXEC=TvShowWatch.spk

syno: TvShowWatch.spk

TvShowWatch.spk: syno/package.tgz syno/INFO syno/scripts syno/PACKAGE_ICON.PNG
	cd syno && tar cvf $@ package.tgz INFO scripts PACKAGE_ICON.PNG
	mv syno/$@ .

syno/package.tar: syno/application LICENSE README.md syno_directory
	tar cvf package.tar *.py LICENSE README.md tpbTSW directory.json
	mv package.tar syno
	cd syno && tar rvf package.tar application

syno/package.tgz: syno/package.tar
	gzip -c syno/package.tar > $@

syno_directory: directory.syno.json
	cp directory.syno.json directory.json
clean:
	rm -rf syno/application/tmp/*
	for i in `find . -name "*.pyc"`; do rm -rf $$i ; done
	for i in `find . -name "*~"`; do rm -rf $$i ; done
	for i in `find . -name "*.xml"`; do rm -rf $i ; done

mrproper: clean
	rm -rf $(EXEC)
	rm -rf syno/package.tar
	rm -rf syno/package.tgz
