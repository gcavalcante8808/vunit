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
    config.set('Vcenter', 'user', vuser)
    config.set('Vcenter', 'pass', vpass)
    config.set('Vcenter', 'server', vserver)

    config.add_section('Host')
    config.set('Host', 'user', huser)
    config.set('Host', 'pass', hpass)
    config.set('Host', 'cluster', hcluster)
    
    with open('vmware.cfg', 'wb') as configfile:
        config.write(configfile)

    return config


def read_vmtest_cfg():
    """ Read the configuration file previously created."""
    config = ConfigParser.RawConfigParser()
    config.read('vmware.cfg')

if __name__ == '__main__':
    pass
