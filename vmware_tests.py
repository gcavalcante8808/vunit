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
This module contains all instructions to test the VMware Infraestructure.
"""
import pickle
import socket
from unittest import TestCase, main
from pysphere import VIServer, VIApiException, VIMor, VIProperty
from manage import read_vmtest_cfg

CREDS = read_vmtest_cfg(cfg="vmware.cfg")

def vcenter_connect():
    """ Connect to the vcenter. """
    server = VIServer()
    server.connect(CREDS.get('Vcenter', 'server'),
                   CREDS.get('Vcenter', 'user'),
                   CREDS.get('Vcenter', 'pass'))

    return server


def host_connect(host):
    """ Connect to a host. """
    server = VIServer()
    server.connect(host, CREDS.get('Host', 'user'),
                   CREDS.get('Host', 'pass'))

    return server


class VmwareBasicTests(TestCase):
    """ Just do all basic tests."""

    def test_user_can_login_on_vcenter(self):
        """Is the Vcenter capable at this moment to login an Active Directory
        User?
        """
        try:
            server = vcenter_connect()
            server.disconnect()
        except VIApiException:
            self.fail("Servidor Indisponivel ou Usuario sem Acesso")

    def test_user_can_login_on_host(self):
        """Local Users can login into hosts separately?"""
        for host in CREDS.get('Host', 'Cluster').split(","):
            try:
                server = host_connect(host)
                server.disconnect()
            except VIApiException:
                self.fail("Service Unavailable or Unknown User/Password")

    def test_vmwareapi_vcenter_type(self):
        """ Is The API Type of 10.61.12.116 a vcenter type?"""
        server = vcenter_connect()
        server_type = server.get_api_type()
        self.assertEqual('VirtualCenter', server_type)
        server.disconnect()

    def test_vmwareapi_host_type(self):
        """ Is the Api of the hosts a Host API Type?"""
        for host in CREDS.get('Host', 'Cluster').split(","):
            server = host_connect(host)
            server_type = server.get_api_type()
            self.assertEqual('HostAgent', server_type)
            server.disconnect()

    def test_vmware_version_vcenter(self):
        """ Is the Vmware version at 5.1?"""
        server = VIServer()
        server.connect(CREDS.get('Vcenter', 'server'),
                       CREDS.get('Vcenter', 'user'),
                       CREDS.get('Vcenter', 'pass'))
        api = server.get_api_version()
        self.assertEqual('5.1', api)
        server.disconnect()

    def test_vmware_version_host(self):
        """ Is the Vmware version at 5.1?"""
        for host in CREDS.get('Host', 'Cluster').split(","):
            server = host_connect(host)
            api = server.get_api_version()
            self.assertEqual('5.1', api)
            server.disconnect()

    def test_and_write_poweredon_vms(self):
        """ Get and write all poweredon vms into a file, that will be used
        later at the VMPowerOn Test."""
        server = vcenter_connect()
        vms = server.get_registered_vms(status='poweredOn')

        with open('vm_number.txt', 'wb') as vm_file:
            pickle.dump(vms, vm_file)

        server.disconnect()

    def test_and_write_datastores(self):
        """Get and write all available datastores into a file."""
        server = vcenter_connect()

        with open('datastores.txt', 'wb') as ds_file:
            pickle.dump(server.get_datastores().values(), ds_file)

        server.disconnect()


#######
####### DIA DE DESLIGAMENTO DO VMWARE
#######

class VmwareTurnOff(TestCase):
    """ Verifica se todas as ações para o desligamento do ambiente foram
        tomadas corretamente."""

    def test_if_vcenter_is_available(self):
        """O Vcenter ainda está ligado?"""
        try:
            server = vcenter_connect()
            server.disconnect()
            self.fail(u"O Vcenter ainda está disponível")
        except socket.error:
            pass

    def test_if_drs_is_deactivated(self):
        """Todos os hosts estão com o DRS desativado?"""
        self.fail('NotImplemented')

    def test_if_all_vms_are_off(self):
        """Todas as máquinas virtuais estão desligadas?"""
        for host in CREDS.get('Host', 'Cluster').split(","):
            server = host_connect(host)
            off = server.get_registered_vms(status='poweredOn')
            self.assertEqual(0, len(off), u"")

    def test_if_all_hosts_are_in_maintenance(self):
        """Todos os hosts estão em modo de manutenção?"""
        server = vcenter_connect()
        hosts = server.get_hosts()

        for host in hosts:
            host_mor = VIMor(host, 'HostSystem')
            host_props = VIProperty(server, host_mor)
            self.assertTrue(host_props.runtime.inMaintenanceMode,
                            u"Nem todos os hosts estão desativados")

#######
####### DIA DE ATIVAÇÃO DO VMWARE
#######

class VmwareTurnOn(TestCase):
    """ Testes a serem realizados após o vmware voltar a ser ligado.
        Estes testes verificam se o ambiente está funcionando da mesma
        forma de antes de ser desligado.
    """

    def setUp(self):
        """Connect To Vmware."""
        self.server = VIServer()
        self.server.connect(CREDS.get('Vcenter', 'server'),
                            CREDS.get('Vcenter', 'user'),
                            CREDS.get('Vcenter', 'pass'))

    def tearDown(self):
        """Disconnects from Vmware."""
        self.server.disconnect()

    def test_if_all_hosts_arent_in_maintenance(self):
        """Todos os hosts estão disponíveis(fora do modo de manutenção)?"""
        hosts = self.server.get_hosts()
        for host in hosts:
            host_mor = VIMor(host, 'HostSystem')
            host_props = VIProperty(self.server, host_mor)
            self.assertFalse(host_props.runtime.inMaintenanceMode,
                             u"Host Not Activated:{}".format(
                                 host))

    def test_if_rfb_datacenter_is_available(self):
        """O datacenter da RFB está disponível?"""
        datacenters = self.server.get_datacenters()
        self.assertEqual('Datacenter RFB', datacenters['datacenter-2'],
                         u"O datacenter da RFB não está disponível")

    def test_if_rfb_cluster_is_available(self):
        """O Cluster da RFB está disponível?"""
        cluster = self.server.get_clusters()
        self.assertEqual('Cluster Receita', cluster['domain-c55'],
                         u"O cluster da RFB não está disponível")

    def test_if_all_previous_poweredOn_machines_are_available(self):
        """As máquinas virtuais ligadas são as mesmas antes da parada?"""
        prev_vms = pickle.load(open('vm_number.txt', 'rb'))
        online_vms = self.server.get_registered_vms(status='poweredOn')
        diff_vms = set(prev_vms).difference(online_vms)
        self.assertEqual(set(), diff_vms, diff_vms)

    def test_if_all_previous_datastores_are_available(self):
        """Os datastores disponíveis são os mesmos de antes da parada?"""
        prev_ds = pickle.load(open('datastores.txt', 'rb'))
        online_ds = self.server.get_datastores().values()
        diff_ds = set(prev_ds).difference(online_ds)
        self.assertEqual(set(), diff_ds, diff_ds)


if __name__ == '__main__':
    main()
