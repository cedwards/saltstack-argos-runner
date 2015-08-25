Argos Orchestration Runner
==========================

Introduction
------------

The Argos runner is a utility for gathering and processing security-related
data from a set of minions. Initially it was designed to gather File Integrity
Monitoring (FIM) data, but has since extended to incorporate CIS benchmarks and
OSquery results. The primary purpose of this tool is to simplify the security
audit workflow by leveraging SaltStack's orchestration framework.

Requirements
------------

This tool leverages a number of components of Salt. These components include:

 - states (tracking changes in managed files)
 - custom execution modules (fim, cis, osquery)
 - orchestration runner (Argos)
 - custom configuration options
 - processing engine (Splunk)

This module was built on 2015.5.x and has been tested on Linux and FreeBSD.

Workflow
--------

The Argos orchestration runner is divided into three main components, and a
fourth combined "audit" process. As described previously, this includes FIM,
CIS and OSquery. These are defined in three different orchestration states,
allowing calls to the three individual tests or combined.

Below are the workflows for each of the main components.

FIM
===

Requirements
------------

* fim.py custom execution module
* minion.d/fim.conf
* fim states 

With these requirements in place the Argos orchestration runner can now collect
and process FIM data. The goal with this release was to gather FIM data on a
daily schedule and submit only the differences between runs. This keeps the
amount of data submitted for processing within Splunk at a minimum, while still
tracking changes to the filesystem.

Workflow
--------

The FIM data is collected and processed by leveraging the `state.orchestrate`
runner. This allows us to define the targets and workflow in a state-like
format. This format is described below:

.. code-block:: yaml

    fim_checksum:
      salt.state:
        - tgt: '*'
        - sls:
          - fim.checksum
    
    cp_push_new:
      salt.function:
        - name: cp.push
        - tgt: '*'
        - arg:
          - {{ salt['config.get']('fim:new_path') }}
        - require:
          - salt: fim_checksum
    
    fim_diff:
      salt.state:
        - tgt: emma
        - sls:
          - fim.diff
        - require:
          - salt: cp_push_new
    
    fim.rotate:
      salt.function:
        - tgt: emma
        - require:
          - salt: fim_diff

