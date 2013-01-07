ifdef ($(LOCALBASE))
	PREFIX=$(LOCALBASE)
else
	PREFIX?=/usr
endif

# checking for python
PYTHONBIN?=$(shell which python3.3)
PYTHONBIN?=$(shell which python3.2)
PYTHONBIN?=$(shell which python3.1)
PYTHONBIN?=$(shell which python3)

ifeq ("$(PYTHONBIN)", "")
$(error Python not found. Version >= 3.0 is required.)
endif

qbiobeat:
	m4 -DLOOK_HERE=$(PREFIX)/share/qbiobeat -DPYTHONBIN=$(PYTHONBIN) -DRUN_THIS=$@.py  pylauncher.in >$@

biorhythm:
	m4 -DLOOK_HERE=$(PREFIX)/share/qbiobeat -DPYTHONBIN=$(PYTHONBIN) -DRUN_THIS=$@.py  pylauncher.in >$@

clean:
	rm qbiobeat biorhythm

install: qbiobeat biorhythm
	# Set up the directories we'll install in
	mkdir -p $(DESTDIR)$(PREFIX)/bin/
	mkdir -p $(DESTDIR)$(PREFIX)/share/qbiobeat
	mkdir -p $(DESTDIR)$(PREFIX)/share/applications
	# Copy over the required files
	install -m644 QBioBeat.desktop $(DESTDIR)$(PREFIX)/share/applications
	install -m644 *.py $(DESTDIR)$(PREFIX)/share/qbiobeat
	install -m755 qbiobeat $(DESTDIR)$(PREFIX)/bin/qbiobeat
	install -m755 biorhythm $(DESTDIR)$(PREFIX)/bin/biorhythm
	#mkdir -p $(DESTDIR)$(PREFIX)/share/icons
	#cp -r hicolor $(DESTDIR)$(PREFIX)/share/icons
