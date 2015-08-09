# -*- coding: utf8 -*-
'''
Salt Runner to collect fim.checksum data
'''
from __future__ import absolute_import

import logging
import salt.client
from time import strftime
from salt.exceptions import SaltClientError

LOG = logging.getLogger(__name__)

__virtualname__ = 'argos'


def __virtual__():
    '''
    Load the argos runner
    '''
    return __virtualname__


def fim(tgt, targets=[], algo='sha256', filename='', *args, **kwargs):
    '''
    FIM collection runner
    '''
    checksum = {}
    timestamp = strftime("%Y-%m-%d %H:%M:%S")

    ## check for preconfigured targets
    if not targets:
        try:
            if __opts__['fim']['targets']:
                targets = __opts__['fim']['targets']
        except:
            return 'No targets defined. Exiting'

    ## check for preconfigured algos
    if not algo:
        try:
            if __opts__['fim']['algo']:
                algo = __opts__['fim']['algo']
        except KeyError:
            LOG.debug('No algorithm defined. Defaulting to sha256')

    ## check for preconfigured filename
    if not filename:
        try:
            if __opts__['fim']['filename']:
                filename = __opts__['fim']['filename']
        except KeyError:
            LOG.debug('No filename defined. Sending to stdout')

    ## spin up Salt client
    client = salt.client.LocalClient()
    try:
        output = client.cmd(tgt, 'fim.checksum', kwarg={'targets': targets, 'algo': algo, 'filename': filename}, timeout=__opts__['timeout'], expr_form='compound')

        ## if filename configured, collect all written files
        if filename:
            collection = client.cmd(tgt, 'cp.push', [filename], timeout=__opts__['timeout'])
            return collection

    except SaltClientError as client_error:
        LOG.debug(client_error)
        return ret

    return output

