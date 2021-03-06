EXEC=TvShowWatch.spk

all: 
	@echo "Usage:"
	@echo "'sudo make install' for root installation. Allow schedule job"
	@echo "'sudo make uninstall' for remove root installation"
	@echo "'make syno' for Synology package TvShowWatch.spk build"

install: script/install.py jsonConfigParser
	@python $<

uninstall: script/uninstall.py
	@python $<
	@rm -rf jsonConfigParser

jsonConfigParser:
	@wget "https://github.com/kavod/jsonSchemaAppGenerator/releases/download/v1.4/jsonConfigParser.tgz" -q -O jsonConfigParser.tar.gz
	@tar zxf jsonConfigParser.tar.gz
	@rm jsonConfigParser.tar.gz

syno: TvShowWatch.spk

TvShowWatch.spk: syno/package.tgz syno/INFO syno/scripts syno/PACKAGE_ICON.PNG
	cd syno && tar cvf $@ package.tgz INFO scripts PACKAGE_ICON.PNG
	mv syno/$@ .

syno/package.tar: application LICENSE README.md syno_directory
	tar cvf package.tar *.py LICENSE README.md directory.json application config-*.jschem
	mv package.tar syno
	cd syno && tar rvf package.tar

syno/package.tgz: syno/package.tar
	gzip -c $< > $@

syno_directory: directory.syno.json
	cp $< directory.json
clean:
	rm -rf application/tmp/*.php
	for i in `find . -name "*.pyc"`; do rm -rf $$i ; done
	for i in `find . -name "*~"`; do rm -rf $$i ; done
	for i in `find . -name "*.xml"`; do rm -rf $i ; done
	for i in `find . -name "*.pid"`; do rm -rf $i ; done

mrproper: clean
	rm -rf $(EXEC)
	rm -rf syno/package.tar
	rm -rf syno/package.tgz
	rm -rf directory.json
	rm -rf paramPy
