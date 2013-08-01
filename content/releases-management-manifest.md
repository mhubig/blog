Title: Release Management Manifest
Date: 2013-06-25
Category: administration, development
Tags: git, release management
Slug: release-management
Author: Markus Hubig
Summary: Ein Vorschlag für ein einfaches Release Management
         Schema für die IMKO GmbH.
status: draft

    :::text
    Author: Markus Hubig
    Date: 2013-06-26
    Draft: 0.1.16

### Vorwort

Im Moment besteht das Problem, dass es sehr viele unterschiedliche Ansätze
dafür gibt, wo und wie Releases unserer Softwarepackete, Firmware Dateien
und Manuals abgelegt werden. Das hat in letzter Zeit immer wieder zu Problemen
geführt. Deswegen haben wir ([Markus](mailto:mhubig@imko.de),
[Nicholas](mailto:ntj@imko.de), [Steven](mailto:so@imko.de) und
[Zhen](mailto:zp@imko.de)) uns ein einfaches Schema zur Ablage und Benennung
überlegt und uns auf dieses als Standart geeinigt.

### Was ist betroffen

Das neue Release-Schema gilt für alle Software Packete, Firmware Dateien,
Hardware Pläne und Protokoll Manuals.

### Das Release-Schema

00. **Zuständigkeit**

    Jeder Entwickler ist für das Release Mangement seiner Software selbst
    verantwortlich!

00. **Zentraler Ort für die Ablage**

    Der Zentrale Ort für die Ablage der Reseases ist von jetzt an die
    **Dropbox**. Und zwar folgende Ordner:

        :::console
        Software: Dropbox/IMKO GmbH (extern)/Software
        Firmware: Dropbox/IMKO GmbH (extern)/Firmware
        Hardware: Dropbox/IMKO GmbH (extern)/Hardware
        Protocol: Dropbox/IMKO GmbH (extern)/Protocol

00. **Namensschema**

    Unterhalb der oben genannten Ordner werden die Dateien nach folgendem
    Schema benannt und abgelegt (mit Beispielen). Dabei halten wir uns bei den
    Versionsnummern an das in
    [Semantic Versioning 2.0.0](http://semver.org/spec/v2.0.0.html)
    vorgeschlagene Schema.

        :::text
                           ,----- Trennzeichen zwischen Name und Version
                           |
                           V
        Kategorie/Name/Name_0.0.0.ext
        --------- ---- ---- - - - ---
        |         |    |    | | | |
        |         |    |    | | | `- Extention (exe, pdf, h86, hex, ...)
        |         |    |    | | `- PATCH (wird bei Bugfixes hochgezählt)
        |         |    |    | `- MINOR (wird bei neuen Features hochgezählt)
        |         |    |    `- MAJOR (bei inkompatiblen API Änderungen)
        |         |    `- Name der Software (Ohne _ , . und Lehrzeichen)
        |         `- Name der Software (Ohne _ , . und Lehrzeichen)
        `- Kategorie (Software, Firmware, Hardware, Protocol)

    Besteht das Release aus mehr als einer Datei, kann natürlich auch alles in
    einem *versionierten Ordner* abgelegt werden. Die Releasedatei **muss**
    aber natürlich trotz allem *versioniert* sein!

        :::console
        Kategorie/Name/Name_0.0.0/Name_0.0.0.ext
        Kategorie/Name/Name_0.0.0/extra-lib.ext
        Kategorie/Name/Name_0.0.0/image.ext
        Kategorie/Name/Name_0.0.0/requirements.txt

    **Beispiele:**

        :::console
        Software/Trime-Tool/Trime-Tool_0.18.9/Trime-Tool_0.18.9.msi
        Firmware/Trime-SONO/Trime-SONO_2.6.6.13.h86
        Protocol/IMPBus2-PICO/IMPBus2-PICO_2.25.0.pdf
        Protocol/IMPBus2-SONO/IMPBus2-SONO_1.3.0.pdf
        Protocol/SDI12-PICO/SDI12-PICO_1.1.0.pdf
        Hardware/Trime-3L/Trime-3L_15.1.0/Trime-3L_15.1.0.sch
        Hardware/Trime-3L/Trime-3L_15.1.0/Trime-3L_15.1.0.brd

00. **Changelog**

    In jedem Namens-Ordner (e.g. `Software/Trime-Tool`) muss sich eine
    `ChangeLog.txt` genannte Datei befinden, in der für jedes neue Release
    ein Eintrag hinzugefügt wird, der die Änderungen zur vorhergehenden
    Version zusammenfasst.

    Dabei ist folgendes Format einzuhalten:

        YYYY-MM-DD MAJOR.MINOR.PATCH, Author Name <email@address.de>

            - COMPONENT: additions

            + COMPONENT: removals

            * COMPONENT: fixes and miscellaneous changes

    Hier ein kleines Beispiel (aus Zhen's TrimeTool `VersionInfo.txt`):

        2012-04-03 0.18.37, Zhen Pei <zp@imko.de>

            * FIX: In Fenster "Basic Balancing" werden die zweien Parameters
                von TDR-Conduct nach dem Eintippen bleiben, wenn die Software
                nicht aus ist.

        2012-04-25 0.18.38, Zhen Pei <zp@imko.de>

            + SERIAL PORT: Hat jetzt zwei Modes für den Serial Port.
                Manual: die Software nutzt den ausgewählten Serial Port.
                Automatisch: die Software sucht den Port automatisch.

    **Tipp:** Wer seinen Quellcode mittels [git](http://git-scm.com) verwaltet,
    kann sich die Einträge für das Changelog File ganz einfach mit Hilfe von
    `git log` erzeugen:

        :::console
        $ git log release-0.8.2..HEAD --reverse --no-merges --pretty=format:'* %s'

        * Adds compatibility for serial urls like 'loop://'
        * Fixes the measure_mode bug!

00. **Abhängigkeiten**

    Eine wichtige Information, die notwendig ist um Softwareprobleme zu
    vermeiden, ist die Dokumentation von Abhängikeiten. Beispiele für solche
    Abhängikeiten sind z.B. `implib2_0.8.5` benötigt `pyserial_2.5` oder neuer.
    Oder `SONO-Config_1.29.0` benötigt mindestens die `PICO-FW_1.140612` oder
    die `SONO-FW_2.060612` oder neuer.

    Diese Abhänigkeiten sollen in der Datei `requirements.txt` dokumentiert
    werden. Diese Datei kann entweder in einem *versionierten Software Ordner*
    abgelegt werden ...

        :::console
        Software/SONO-Config/ChangeLog.txt
        Software/SONO-Config/SONO-Config_1.29.0/SONO-Config_1.29.0.msi
        Software/SONO-Config/SONO-Config_1.29.0/requirements.txt

    ... oder selbst *versioniert* werden.

        :::console
        Software/SONO-Config/ChangeLog.txt
        Software/SONO-Config/SONO-Config_1.29.0.msi
        Software/SONO-Config/requirements_1.29.0.txt

    Diese Datei beinhaltet dann für jede Abhänigkeit eine Zeile. Diese Zeilen
    bestehen aus der Bezeichnug der Abhänigket, einem relationalen Operator
    (`==`, `>=`, `<=`, `!=`) und der Bezugs-Version. Beispiele:

        :::python
        pyserial>=2.5

        picofw>=1.140612
        sonofw>=2.060612

        sonohw>=1.14.6
        picohw>=2.6.12

        sono-impbus2==1.3
        pico-impbus2==0.25

    Dabei gilt, dass nicht spezifizierte Stellen wie Platzhalter wirken:

        :::python
        sono-impbus2==1.3: sono-impbus2_1.3.1   => OK
        sono-impbus2==1.3: sono-impbus2_1.3.999 => OK

    Bezeichnungen können auch mehrmals genutzt werden, z.B.:

        :::python
        pyserial>=2.5
        pyserial<=3.0
        pyserial!=2.5.1
        pyserial!=2.5.76

00. **Checksum**

    Um die Korrecktheit der Dateien verifizierbar zu machen, ist es nötig für
    Jede Release-Datei eine Checksummen zu berechnen und zusammen mit dieser
    abzuspeichern. *State of the Art* is heutzutage eine mit dem
    [sha512](https://de.wikipedia.org/wiki/SHA-2) Algorythmus berechnete
    Checksumme.

    #### Erzeugen und Verifizieren der Checksumme unter Windows

    Unter Windows kann eine sha512 Checksumme ganz einfach mit dem
    [File Checksum Tool](http://www.krylack.com/file-checksum-tool/) erzeugt
    werden:

    ![](http://www.krylack.com/images/file-checksum-tool-screenshot.jpg)

    #### Erzeugen und Verifizieren der Checksumme unter Linux

        :::console
        $ sha512sum Pico-BT_1.18.0.elf > Pico-BT_1.18.0.elf.sha512
        $ sha512sum -c  Pico-BT_1.18.0.elf.sha512
        Pico-BT_1.18.0.elf: OK

    Oder für einen ganzen Ordner:

        :::console
        $ sha512sum SONO-View_1.0.0/* > SONO-View_1.0.0.sha512
        $ sha512sum -c SONO-View_1.0.0.sha512
        SONO-View_1.0.0/AVRootloader.dev: OK
        SONO-View_1.0.0/AVRootloader.exe: OK
        SONO-View_1.0.0/AVRootloader.ini: OK
        SONO-View_1.0.0/SView_APP_1.0.0.hex: OK
        SONO-View_1.0.0/SView_IBT_1.0.0.hex: OK
        SONO-View_1.0.0/requirements.txt: OK

    #### Erzeugen und Verifizieren der Checksumme unter Mac OS X

        ::::console
        $ shasum -a 512 Pico-BT_1.18.0.elf > Pico-BT_1.18.0.elf.sha512
        $ shasum -a 512 -c Pico-BT_1.18.0.elf.sha512
        Pico-BT_1.18.0.elf: OK

    Oder für einen ganzen Ordner:

        :::console
        $ shasum -a 512 SONO-View_1.0.0/* > SONO-View_1.0.0.sha512
        $ shasum -a 512 -c SONO-View_1.0.0.sha512
        SONO-View_1.0.0/AVRootloader.dev: OK
        SONO-View_1.0.0/AVRootloader.exe: OK
        SONO-View_1.0.0/AVRootloader.ini: OK
        SONO-View_1.0.0/SView_APP_1.0.0.hex: OK
        SONO-View_1.0.0/SView_IBT_1.0.0.hex: OK
        SONO-View_1.0.0/requirements.txt: OK

    #### Namensschema für die Checksummen Datei

    - Für eine einzelne Datei: `<filename>.<ext>.sha512`
    - Für einen ganzen Ordner: `<directoryname>.sha512`
