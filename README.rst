============
Dump Aliases
============

On FreeBSD's postfix, /etc/aliases will be compiled into /etc/aliases.db,

but there is no easy way to access it (e.g. dump the content of a mailing list)

this repo is trying to dump it, that's all.

Output Format
-------------

For all email address that is in a mailing list, output

<list>:<address>

for example, if an email address, say python@hello.world, is in two mailing lists on this machine, say list1 and list2, the output should be ::

    list1:python@hello.world
    list2:python@hello.world

No matter whether list1 is in list2 or list2 is in list1.
