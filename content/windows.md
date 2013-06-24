Title: HowTo create a multiversion Windows 7 ISO-Image on Mac
Date: 2013-06-20
Category: administration
Tags: windows7, installation
Slug: multiversion-windows7-iso
Author: Markus Hubig
Summary: Step for step guide of how to create a multiversion
         Windows 7 ISO-Image using a Mac.

00. Use Homebrew to install mkisofs:

        $ brew install cdrtools

00. Create a new directory:

        $ mkdir win7 && cd win7

00. Download the Windows 7 DE SP1 ISO-Image:

        $ wget http://msft.digitalrivercontent.net/win/X17-24289.iso (x64)
        $ wget http://msft.digitalrivercontent.net/win/X17-24288.iso (x86)

00. Mount the ISO-Image and copy it's content to disk:

        $ hdiutil mount X17-24289.iso
        /dev/disk4  /Volumes/GRMCPRXFRER_DE_DVD
        $ mkdir copy
        $ cp -a /Volumes/GRMCPRXFRER_DE_DVD/* copy/
        $ cd copy/

00. Delete the `ei.cfg` file:

        $ rm -f sources/ei.cfg

00. And make a new and bootable ISO-Image:

        $ mkisofs -o ../win7.iso -b boot/etfsboot.com -no-emul-boot \
          -c BOOT.CAT -iso-level 2 -udf -J -l -D -N -joliet-long \
          -relaxed-filenames .
        $ cd ..

00. Now burn it to a DVD with:

        $ hdiutil burn win7.iso
