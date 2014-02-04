#!/usr/bin/env python
# -*- coding: utf-8 -*-
#__author__ = '01388863189'
#
# Done by Gabriel Abdalla Cavalcante Silva at Receita Federal do Brasil,
#
# Licensed under the Apache License, Version 2.0, that can be viewed at:
#   http://www.apache.org/licenses/LICENSE-2.0
#
"""
Tests the manage module and the vmware_tests.py module.
"""
import unittest
import ConfigParser
from manage import create_vmtest_cfg


class ManagementFunctionsTest(unittest.TestCase):
    """ Contains all manage tests."""
    def setUp(self):
        self.vcenter_user = 'vcenter'
        self.vcenter_pass = 'vcenter123'
        self.vcenter_server = 'vcenter.domain.com'

        self.esxi_user = 'esxi'
        self.esxi_pass = 'esxi123'
        self.esxi_hosts = ['host1', 'host2', ]

    def test_create_vmtest_cfg(self):
        """ Test if the create_vmtest_cfg works as expected. """
        cfg = create_vmtest_cfg(self.vcenter_user,
                                self.vcenter_pass,
                                self.vcenter_server,
                                self.esxi_user,
                                self.esxi_pass,
                                self.esxi_hosts)

        self.assertIsInstance(cfg, ConfigParser.RawConfigParser)
        self.assertTrue(cfg.has_section('Vcenter'))
        self.assertTrue(cfg.has_section('Host'))

        self.assertEqual(self.vcenter_user, cfg.get('Vcenter', 'user'))
        self.assertEqual(self.vcenter_pass, cfg.get('Vcenter', 'pass'))
        self.assertEqual(self.vcenter_server, cfg.get('Vcenter', 'server'))

        self.assertEqual(self.esxi_user, cfg.get('Host', 'user'))
        self.assertEqual(self.esxi_pass, cfg.get('Host', 'pass'))
        self.assertEqual(self.esxi_hosts, cfg.get('Host', 'cluster'))

        c = ConfigParser.RawConfigParser()
        c.read('vmware.cfg')
        self.assertTrue(c)


if __name__ == '__main__':
    unittest.main()
