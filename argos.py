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
    Load the fim client
    '''
    return __virtualname__


def _get_targets():
    '''
    Query master config for possible config options
    '''
    targets = []
    if __opts__['fim']['targets']:
        targets = __opts__['fim']['targets']

    return targets


def _get_algo():
    '''
    Query master config for possible config options
    '''
    algo = ''
    if __opts__['fim']['algo']:
        algo = __opts__['fim']['algo']

    return algo


def panoptes(tgt, targets=[], algo='', *args, **kwargs):
    '''
    Too soon!
    '''
    checksum = {}
    timestamp = strftime("%Y-%m-%d %H:%M:%S")

    if not targets:
        targets = _get_targets()

    if not algo:
        algo = _get_algo()

    client = salt.client.LocalClient()
    try:
        output = client.cmd(tgt, 'fim.checksum', kwarg={'targets': targets, 'algo': algo}, timeout=__opts__['timeout'], expr_form='compound')
        for minion, target in output.iteritems():
            checksum.update({minion: {'files': []}})
            for path, stats in target.iteritems():
                checksum[minion]['files'].append(stats)
            checksum[minion]['files'].append({'timestamp':timestamp})

    except SaltClientError as client_error:
        LOG.debug(client_error)
        return ret

    return checksum

