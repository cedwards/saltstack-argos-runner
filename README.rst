Salt Runner to collect FIM output
=================================

This module is a Salt runner that gathers output from the FIM module and
collects it in a central place. This can be used with a returner to be consumed
and parsed by some analytics engine (think Splunk).

Requirements
------------

This module, as it runs on the master, needs to be available in the
```extension_modules``` directory as defined in the master config file. I
generally standardize this path at: ```/etc/salt/master.d/extmods/```. This
file would need to be placed in ```${extension_modules}/runners```.

This module also requires the FIM execution module on each minion that wants to
be tracked. The FIM module documentation can be found in that repository.

Configuration
-------------

This runner has an optional config file where a few options can be defined.
These options define the hashing algorithm and list of files / directories that
you'd like to track. Example:

.. code-block:: yaml

    fim:
      algo: sha256
      targets:
        - /etc/shadow
        - /etc/passwd
        - /usr/local/bin
        - /usr/local/etc

Command Line Options
--------------------

If you select not to hard-code your algorithm and targets in the config, the
runner takes these as arguments at runtime. These are used as follows:

.. code-block:: shell

    salt-run argos.panoptes '*' targets='['/path/1', '/path/2', '/dir/']' algo='sha256'

It is possible to only hard-code one or the other of the option, but you'll
need to provide that argument on the command line at runtime.
