title: Install and setup Samba and OpenLDAP
date: 2013-06-20
category: administration
tags: samba, ldap
slug: samba-openldap-nis
author: Markus Hubig
summary: Short step-for-step guide on how to install Samba with OpenLDAP
         authentication and setup Ubuntu to also use OpenLDAP for user
         management.

### Install Samba, OpenLDAP

00. `$ sudo apt-get install samba-common samba`
00. `$ sudo apt-get install slapd ldap-util smbldap-tools`

### Configure OpenLDAP

00. Install the samba schema. The schema is found in the installed
   `samba-doc` package. It needs to be unzipped and copied to the
   `/etc/ldap/schema` directory

        $ sudo cp /usr/share/doc/samba-doc/examples/LDAP/samba.schema.gz \
          /etc/ldap/schema
        $ sudo gzip -d /etc/ldap/schema/samba.schema.gz

00. Have the configuration file schema_convert.conf that contains the
    following lines:

        include /etc/ldap/schema/core.schema
        include /etc/ldap/schema/collective.schema
        include /etc/ldap/schema/corba.schema
        include /etc/ldap/schema/cosine.schema
        include /etc/ldap/schema/duaconf.schema
        include /etc/ldap/schema/dyngroup.schema
        include /etc/ldap/schema/inetorgperson.schema
        include /etc/ldap/schema/java.schema
        include /etc/ldap/schema/misc.schema
        include /etc/ldap/schema/nis.schema
        include /etc/ldap/schema/openldap.schema
        include /etc/ldap/schema/ppolicy.schema
        include /etc/ldap/schema/ldapns.schema
        include /etc/ldap/schema/pmi.schema
        include /etc/ldap/schema/samba.schema

00. Create a directory `ldif_output` to hold the output.
        $ mkdir ldif_output

00. Determine the index of the schema (`{14}` in this case):

        $ slapcat -f schema_convert.conf -F ldif_output -n0 -H \
          ldap:///cn={14}samba,cn=schema,cn=config -l cn=samba.ldif

00. Convert the schema to LDIF format:

        $ slapcat -f schema_convert.conf -F ldif_output -n0 -H \
          ldap:///cn={14}samba,cn=schema,cn=config -l cn=samba.ldif

00. Edit the generated cn=samba.ldif file by removing index information
    (`{14}`) at:

        dn: cn=samba,cn=schema,cn=config
        ...
        cn: samba

    Remove the bottom lines:

        structuralObjectClass: olcSchemaConfig
        entryUUID: b53b75ca-083f-102d-9fff-2f64fd123c95
        creatorsName: cn=config
        createTimestamp: 20080827045234Z
        entryCSN: 20080827045234.341425Z#000000#000#000000
        modifiersName: cn=config
        modifyTimestamp: 20080827045234Z

00. Add the new schema:

        $ sudo ldapadd -Q -Y EXTERNAL -H ldapi:/// -f cn\=samba.ldif

    To query and view this new schema:

        $ sudo ldapsearch -Q -LLL -Y EXTERNAL -H ldapi:/// -b cn=schema,cn=config 'cn=*samba*'

00. Create the file `samba_indices.ldif` with the following contents:

        dn: olcDatabase={1}hdb,cn=config
        changetype: modify
        add: olcDbIndex
        olcDbIndex: uidNumber eq
        olcDbIndex: gidNumber eq
        olcDbIndex: loginShell eq
        olcDbIndex: uid eq,pres,sub
        olcDbIndex: memberUid eq,pres,sub
        olcDbIndex: uniqueMember eq,pres
        olcDbIndex: sambaSID eq
        olcDbIndex: sambaPrimaryGroupSID eq
        olcDbIndex: sambaGroupType eq
        olcDbIndex: sambaSIDList eq
        olcDbIndex: sambaDomainName eq
        olcDbIndex: default sub

00. Use the ldapmodify utility to load the new indices:

        $ sudo ldapmodify -Q -Y EXTERNAL -H ldapi:/// -f samba_indices.ldif

    If all went well you should see the new indices using ldapsearch:

        $ sudo ldapsearch -Q -LLL -Y EXTERNAL -H \
          ldapi:/// -b cn=config olcDatabase={1}hdb olcDbIndex

Replay the LDAP Backup
======================

00. Create a Backup on the old LDAP Server with `slapcat`:

        $ sudo slapcat > backup.ldap

00. Copy the backup to the new Server with `scp`:

        $ scp backup.ldap imko@fileserver.imko:

00. Edit the `backup.ldap` file and remove the `dc`-root:

        > dn: dc=imko
        > objectClass: dcObject
        > objectClass: organization
        > o: imko
        > dc: imko
        > structuralObjectClass: organization
        > entryUUID: b5d2fd4a-e9a7-102a-9fce-e096f65474c8
        > creatorsName: cn=admin,dc=imko
        > createTimestamp: 20061006165901Z
        > entryCSN: 20061006165901.000000Z#000001#000#000000
        > modifiersName: cn=admin,dc=imko
        > modifyTimestamp: 20061006165901Z

00. Stop the `slapd` server and replay the backup:

        $ sudo service slapd stop
        $ sudo slapadd -l backup.ldap


