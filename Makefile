EXEC=TvShowWatch.spk

all: 
	@echo "Usage:"
	@echo "'sudo make install' for root installation. Allow schedule job"
	@echo "'sudo make uninstall' for remove root installation"
	@echo "'make user_install' for user installation (using public_html). No scheduled tracking"
	@echo "'make user_uninstall' for remove user installation"
	@echo "'make syno' for Synology package TvShowWatch.spk build"

user_install: script/user_install.sh
	@./script/user_install.sh

user_uninstall: script/user_uninstall.sh
	@./script/user_uninstall.sh

install: script/install.sh
	@./script/install.sh

uninstall: script/uninstall.sh
	@./script/uninstall.sh

syno: TvShowWatch.spk

TvShowWatch.spk: syno/package.tgz syno/INFO syno/scripts syno/PACKAGE_ICON.PNG
	cd syno && tar cvf $@ package.tgz INFO scripts PACKAGE_ICON.PNG
	mv syno/$@ .

syno/package.tar: application LICENSE README.md syno_directory
	tar cvf package.tar *.py LICENSE README.md tpbTSW directory.json application
	mv package.tar syno
	cd syno && tar rvf package.tar

syno/package.tgz: syno/package.tar
	gzip -c syno/package.tar > $@

syno_directory: directory.syno.json
	cp directory.syno.json application/api/directory.json
clean:
	rm -rf application/tmp/*.php
	for i in `find . -name "*.pyc"`; do rm -rf $$i ; done
	for i in `find . -name "*~"`; do rm -rf $$i ; done
	for i in `find . -name "*.xml"`; do rm -rf $i ; done

mrproper: clean
	rm -rf $(EXEC)
	rm -rf syno/package.tar
	rm -rf syno/package.tgz
