PREFIX := /usr

install: all
	mkdir -p $(DESTDIR)$(PREFIX)/bin/
	#mkdir -p $(DESTDIR)$(PREFIX)/share/icons
	mkdir -p $(DESTDIR)$(PREFIX)/share/qbiobeat
	install -Dm644 *.py $(DESTDIR)$(PREFIX)/share/qbiobeat
	install -Dm755 biorhythm.py $(DESTDIR)$(PREFIX)/share/qbiobeat/biorhythm.py
	install -Dm755 qbiobeat.py $(DESTDIR)$(PREFIX)/share/qbiobeat/qbiobeat.py
	#cp -r hicolor $(DESTDIR)$(PREFIX)/share/icons
	ln -s $(PREFIX)/share/qbiobeat/qbiobeat.py $(PREFIX)/bin/qbiobeat
	ln -s $(PREFIX)/share/qbiobeat/biorhythm.py $(PREFIX)/bin/biorhythm
