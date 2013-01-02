PREFIX := /usr

install:
	mkdir -p $(DESTDIR)$(PREFIX)/bin/
	mkdir -p $(DESTDIR)$(PREFIX)/share/qbiobeat
	install -Dm644 *.py $(DESTDIR)$(PREFIX)/share/qbiobeat
	install -Dm755 biorhythm.py $(DESTDIR)$(PREFIX)/share/qbiobeat/biorhythm.py
	install -Dm755 qbiobeat.py $(DESTDIR)$(PREFIX)/share/qbiobeat/qbiobeat.py
	ln -s $(PREFIX)/share/qbiobeat/qbiobeat.py $(DESTDIR)$(PREFIX)/bin/qbiobeat
	ln -s $(PREFIX)/share/qbiobeat/biorhythm.py $(DESTDIR)$(PREFIX)/bin/biorhythm
	#mkdir -p $(DESTDIR)$(PREFIX)/share/icons
	#cp -r hicolor $(DESTDIR)$(PREFIX)/share/icons
