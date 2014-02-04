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


def create_vmtest_cfg(vuser, vpass, vserver, huser, hpass, hcluster):
    """ Create a new configuration file;if it exists, it will be overwritten."""
    config = ConfigParser.RawConfigParser()
    config.add_section('Vcenter')
    config.set('Vcenter', 'user', 'service_dsim@rfoc.srf')
    config.set('Vcenter', 'pass', 'Receita123@difra')
    config.add_section('Host')
    config.set('Host', 'user', 'service_dsim@rfoc.srf')
    config.set('Host', 'user', 'rfbV3RO')
    config.set('Host', 'pass', 'Receita123$')
    config.set('Host', 'cluster', ['10.61.12.109', '10.61.12.110',
                                         '10.61.12.111', '10.61.12.113',
                                         '10.61.12.114', '10.61.12.115'])
    with open('vmware.cfg', 'wb') as configfile:
        config.write(configfile)

    return config


def read_vmtest_cfg():
    """ Read the configuration file previously created."""
    config = ConfigParser.RawConfigParser()
    config.read('vmware.cfg')

if __name__ == '__main__':
    pass
