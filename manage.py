#!/usr/bin/env python
# -*- coding: utf-8 -*-
#__author__ = '01388863189'
#
# Done by Gabriel Abdalla Cavalcante Silva at Receita Federal do Brasil,
#
# Licensed under the Apache License, Version 2.0, that can be viewed at:
#   http://www.apache.org/licenses/LICENSE-2.0
""" This module contain all functions neeeded to configure the environment
    to evaluate the Tests with success.
"""
import ConfigParser


def create_vmtest_cfg(**kwargs):
    """ Create a new configuration file;if it exists, it will be overwritten."""
    config = ConfigParser.ConfigParser()
    config.add_section('Vcenter')
    config.set('Vcenter', 'user', kwargs['vuser'])
    config.set('Vcenter', 'pass', kwargs['vpass'])
    config.set('Vcenter', 'server', kwargs['vserver'])
    config.set('Vcenter', 'datacenter', kwargs['vdcenter'])
    config.set('Vcenter', 'cluster', kwargs['vdcluster'])

    config.add_section('Host')
    config.set('Host', 'user', kwargs['huser'])
    config.set('Host', 'pass', kwargs['hpass'])
    config.set('Host', 'cluster', kwargs['hcluster'])

    with open(kwargs['cfg'], 'wb') as configfile:
        config.write(configfile)

    if kwargs.get('debug', None):
        return config


def read_vmtest_cfg(**kwargs):
    """ Read the configuration file previously created."""
    config = ConfigParser.ConfigParser()
    config.read(kwargs['cfg'])

    return config

if __name__ == '__main__':
    pass