.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV

=====================
Patrole Tempest Tests
=====================

Scope
=====

This test area evaluates the ability of a system under test to support the
role-based access control (RBAC) implementation.
The test area specifically validates services image and networking.


References
================

- `OpenStack image service API reference <https://developer.openstack.org/api-ref/image/v2/index.html>`_
- `OpenStack metadata definitions service API reference <https://developer.openstack.org/api-ref/image/v2/metadefs-index.html>`_
- `OpenStack layer 2 networking service API reference <https://developer.openstack.org/api-ref/network/v2/index.html#layer-2-networking>`_
- `OpenStack layer 3 networking service API reference <https://developer.openstack.org/api-ref/network/v2/index.html#layer-3-networking>`_
- `OpenStack network security API reference <https://developer.openstack.org/api-ref/network/v2/index.html#security>`_
- `OpenStack resource management API reference <https://developer.openstack.org/api-ref/network/v2/index.html#resource-management>`_
- `OpenStack networking agents API reference <https://developer.openstack.org/api-ref/network/v2/index.html#networking-agents>`_


System Under Test (SUT)
=======================

The system under test is assumed to be the NFVI and VIM deployed on a Pharos
compliant infrastructure.


Test Area Structure
====================

The test area is structured in individual tests as listed below. Each test case
is able to run independently, i.e. irrelevant of the state created by a previous
test. For detailed information on the individual steps and assertions performed
by the tests, review the Python source code accessible via the following links.

**Image basic RBAC test:**

These tests cover the RBAC tests of image basic operations.

Implementation:
`BasicOperationsImagesRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/image/test_images_rbac.py>`_

- patrole_tempest_plugin.tests.api.image.test_images_rbac.BasicOperationsImagesRbacTest.test_create_image
- patrole_tempest_plugin.tests.api.image.test_images_rbac.BasicOperationsImagesRbacTest.test_create_image_tag
- patrole_tempest_plugin.tests.api.image.test_images_rbac.BasicOperationsImagesRbacTest.test_deactivate_image
- patrole_tempest_plugin.tests.api.image.test_images_rbac.BasicOperationsImagesRbacTest.test_delete_image
- patrole_tempest_plugin.tests.api.image.test_images_rbac.BasicOperationsImagesRbacTest.test_delete_image_tag
- patrole_tempest_plugin.tests.api.image.test_images_rbac.BasicOperationsImagesRbacTest.test_download_image
- patrole_tempest_plugin.tests.api.image.test_images_rbac.BasicOperationsImagesRbacTest.test_list_images
- patrole_tempest_plugin.tests.api.image.test_images_rbac.BasicOperationsImagesRbacTest.test_publicize_image
- patrole_tempest_plugin.tests.api.image.test_images_rbac.BasicOperationsImagesRbacTest.test_reactivate_image
- patrole_tempest_plugin.tests.api.image.test_images_rbac.BasicOperationsImagesRbacTest.test_show_image
- patrole_tempest_plugin.tests.api.image.test_images_rbac.BasicOperationsImagesRbacTest.test_update_image
- patrole_tempest_plugin.tests.api.image.test_images_rbac.BasicOperationsImagesRbacTest.test_upload_image


**Image namespaces RBAC test:**

These tests cover the RBAC tests of image namespaces.

Implementation:
`ImageNamespacesRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/image/test_image_namespace_rbac.py>`_

- patrole_tempest_plugin.tests.api.image.test_image_namespace_rbac.ImageNamespacesRbacTest.test_create_metadef_namespace
- patrole_tempest_plugin.tests.api.image.test_image_namespace_rbac.ImageNamespacesRbacTest.test_list_metadef_namespaces
- patrole_tempest_plugin.tests.api.image.test_image_namespace_rbac.ImageNamespacesRbacTest.test_modify_metadef_namespace


**Image namespaces objects RBAC test:**

These tests cover the RBAC tests of image namespaces objects.

Implementation:
`ImageNamespacesObjectsRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/image/test_image_namespace_objects_rbac.py>`_

- patrole_tempest_plugin.tests.api.image.test_image_namespace_objects_rbac.ImageNamespacesObjectsRbacTest.test_create_metadef_object_in_namespace
- patrole_tempest_plugin.tests.api.image.test_image_namespace_objects_rbac.ImageNamespacesObjectsRbacTest.test_list_metadef_objects_in_namespace
- patrole_tempest_plugin.tests.api.image.test_image_namespace_objects_rbac.ImageNamespacesObjectsRbacTest.test_show_metadef_object_in_namespace
- patrole_tempest_plugin.tests.api.image.test_image_namespace_objects_rbac.ImageNamespacesObjectsRbacTest.test_update_metadef_object_in_namespace


**Image namespaces property RBAC test:**

These tests cover the RBAC tests of image namespaces property.

Implementation:
`NamespacesPropertyRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/image/test_image_namespace_property_rbac.py>`_

- patrole_tempest_plugin.tests.api.image.test_image_namespace_property_rbac.NamespacesPropertyRbacTest.test_add_md_properties
- patrole_tempest_plugin.tests.api.image.test_image_namespace_property_rbac.NamespacesPropertyRbacTest.test_get_md_properties
- patrole_tempest_plugin.tests.api.image.test_image_namespace_property_rbac.NamespacesPropertyRbacTest.test_get_md_property
- patrole_tempest_plugin.tests.api.image.test_image_namespace_property_rbac.NamespacesPropertyRbacTest.test_modify_md_properties


**Image namespaces tags RBAC test:**

These tests cover the RBAC tests of image namespaces tags.

Implementation:
`NamespaceTagsRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/image/test_image_namespace_tags_rbac.py>`_

- patrole_tempest_plugin.tests.api.image.test_image_namespace_tags_rbac.NamespaceTagsRbacTest.test_create_namespace_tag
- patrole_tempest_plugin.tests.api.image.test_image_namespace_tags_rbac.NamespaceTagsRbacTest.test_create_namespace_tags
- patrole_tempest_plugin.tests.api.image.test_image_namespace_tags_rbac.NamespaceTagsRbacTest.test_list_namespace_tags
- patrole_tempest_plugin.tests.api.image.test_image_namespace_tags_rbac.NamespaceTagsRbacTest.test_show_namespace_tag
- patrole_tempest_plugin.tests.api.image.test_image_namespace_tags_rbac.NamespaceTagsRbacTest.test_update_namespace_tag


**Image resource types RBAC test:**

These tests cover the RBAC tests of image resource types.

Implementation:
`ImageResourceTypesRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/image/test_image_resource_types_rbac.py>`_

- patrole_tempest_plugin.tests.api.image.test_image_resource_types_rbac.ImageResourceTypesRbacTest.test_add_metadef_resource_type
- patrole_tempest_plugin.tests.api.image.test_image_resource_types_rbac.ImageResourceTypesRbacTest.test_get_metadef_resource_type
- patrole_tempest_plugin.tests.api.image.test_image_resource_types_rbac.ImageResourceTypesRbacTest.test_list_metadef_resource_types


**Image member RBAC test:**

These tests cover the RBAC tests of image member.

Implementation:
`ImagesMemberRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/image/test_images_member_rbac.py>`_

- patrole_tempest_plugin.tests.api.image.test_images_member_rbac.ImagesMemberRbacTest.test_add_image_member
- patrole_tempest_plugin.tests.api.image.test_images_member_rbac.ImagesMemberRbacTest.test_delete_image_member
- patrole_tempest_plugin.tests.api.image.test_images_member_rbac.ImagesMemberRbacTest.test_list_image_members
- patrole_tempest_plugin.tests.api.image.test_images_member_rbac.ImagesMemberRbacTest.test_show_image_member


**Network agents RBAC test:**

These tests cover the RBAC tests of network agents.

Implementation:
`AgentsRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/network/test_agents_rbac.py#L24>`_ and
`DHCPAgentSchedulersRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/network/test_agents_rbac.py#L147>`_.

- patrole_tempest_plugin.tests.api.network.test_agents_rbac.AgentsRbacTest.test_show_agent
- patrole_tempest_plugin.tests.api.network.test_agents_rbac.AgentsRbacTest.test_update_agent
- patrole_tempest_plugin.tests.api.network.test_agents_rbac.DHCPAgentSchedulersRbacTest.test_add_dhcp_agent_to_network
- patrole_tempest_plugin.tests.api.network.test_agents_rbac.DHCPAgentSchedulersRbacTest.test_delete_network_from_dhcp_agent
- patrole_tempest_plugin.tests.api.network.test_agents_rbac.DHCPAgentSchedulersRbacTest.test_list_networks_hosted_by_one_dhcp_agent


**Network floating ips RBAC test:**

These tests cover the RBAC tests of network floating ips.

Implementation:
`FloatingIpsRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/network/test_floating_ips_rbac.py>`_

- patrole_tempest_plugin.tests.api.network.test_floating_ips_rbac.FloatingIpsRbacTest.test_create_floating_ip
- patrole_tempest_plugin.tests.api.network.test_floating_ips_rbac.FloatingIpsRbacTest.test_create_floating_ip_floatingip_address
- patrole_tempest_plugin.tests.api.network.test_floating_ips_rbac.FloatingIpsRbacTest.test_delete_floating_ip
- patrole_tempest_plugin.tests.api.network.test_floating_ips_rbac.FloatingIpsRbacTest.test_show_floating_ip
- patrole_tempest_plugin.tests.api.network.test_floating_ips_rbac.FloatingIpsRbacTest.test_update_floating_ip


**Network basic RBAC test:**

These tests cover the RBAC tests of network basic operations.

Implementation:
`NetworksRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/network/test_networks_rbac.py>`_

- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_create_network
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_create_network_provider_network_type
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_create_network_provider_segmentation_id
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_create_network_router_external
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_create_network_shared
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_create_subnet
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_delete_network
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_delete_subnet
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_list_dhcp_agents_on_hosting_network
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_show_network
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_show_network_provider_network_type
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_show_network_provider_physical_network
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_show_network_provider_segmentation_id
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_show_network_router_external
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_show_subnet
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_update_network
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_update_network_router_external
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_update_network_shared
- patrole_tempest_plugin.tests.api.network.test_networks_rbac.NetworksRbacTest.test_update_subnet


**Network ports RBAC test:**

These tests cover the RBAC tests of network ports.

Implementation:
`PortsRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/network/test_ports_rbac.py>`_

- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_create_port
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_create_port_allowed_address_pairs
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_create_port_binding_host_id
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_create_port_binding_profile
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_create_port_device_owner
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_create_port_fixed_ips
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_create_port_mac_address
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_create_port_security_enabled
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_delete_port
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_show_port
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_show_port_binding_host_id
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_show_port_binding_profile
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_show_port_binding_vif_details
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_show_port_binding_vif_type
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_update_port
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_update_port_allowed_address_pairs
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_update_port_binding_host_id
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_update_port_binding_profile
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_update_port_device_owner
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_update_port_fixed_ips
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_update_port_mac_address
- patrole_tempest_plugin.tests.api.network.test_ports_rbac.PortsRbacTest.test_update_port_security_enabled


**Network routers RBAC test:**

These tests cover the RBAC tests of network routers.

Implementation:
`RouterRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/network/test_routers_rbac.py>`_

- patrole_tempest_plugin.tests.api.network.test_routers_rbac.RouterRbacTest.test_add_router_interface
- patrole_tempest_plugin.tests.api.network.test_routers_rbac.RouterRbacTest.test_create_router
- patrole_tempest_plugin.tests.api.network.test_routers_rbac.RouterRbacTest.test_create_router_enable_snat
- patrole_tempest_plugin.tests.api.network.test_routers_rbac.RouterRbacTest.test_create_router_external_fixed_ips
- patrole_tempest_plugin.tests.api.network.test_routers_rbac.RouterRbacTest.test_delete_router
- patrole_tempest_plugin.tests.api.network.test_routers_rbac.RouterRbacTest.test_remove_router_interface
- patrole_tempest_plugin.tests.api.network.test_routers_rbac.RouterRbacTest.test_show_router
- patrole_tempest_plugin.tests.api.network.test_routers_rbac.RouterRbacTest.test_update_router
- patrole_tempest_plugin.tests.api.network.test_routers_rbac.RouterRbacTest.test_update_router_enable_snat
- patrole_tempest_plugin.tests.api.network.test_routers_rbac.RouterRbacTest.test_update_router_external_fixed_ips
- patrole_tempest_plugin.tests.api.network.test_routers_rbac.RouterRbacTest.test_update_router_external_gateway_info
- patrole_tempest_plugin.tests.api.network.test_routers_rbac.RouterRbacTest.test_update_router_external_gateway_info_network_id


**Network security groups RBAC test:**

These tests cover the RBAC tests of network security groups.

Implementation:
`SecGroupRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/network/test_security_groups_rbac.py>`_

- patrole_tempest_plugin.tests.api.network.test_security_groups_rbac.SecGroupRbacTest.test_create_security_group
- patrole_tempest_plugin.tests.api.network.test_security_groups_rbac.SecGroupRbacTest.test_create_security_group_rule
- patrole_tempest_plugin.tests.api.network.test_security_groups_rbac.SecGroupRbacTest.test_delete_security_group
- patrole_tempest_plugin.tests.api.network.test_security_groups_rbac.SecGroupRbacTest.test_delete_security_group_rule
- patrole_tempest_plugin.tests.api.network.test_security_groups_rbac.SecGroupRbacTest.test_list_security_group_rules
- patrole_tempest_plugin.tests.api.network.test_security_groups_rbac.SecGroupRbacTest.test_list_security_groups
- patrole_tempest_plugin.tests.api.network.test_security_groups_rbac.SecGroupRbacTest.test_show_security_group_rule
- patrole_tempest_plugin.tests.api.network.test_security_groups_rbac.SecGroupRbacTest.test_show_security_groups
- patrole_tempest_plugin.tests.api.network.test_security_groups_rbac.SecGroupRbacTest.test_update_security_group


**Network service providers RBAC test:**

These tests cover the RBAC tests of network service providers.

Implementation:
`ServiceProvidersRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/network/test_service_providers_rbac.py>`_

- patrole_tempest_plugin.tests.api.network.test_service_providers_rbac.ServiceProvidersRbacTest.test_list_service_providers


**Network subnetpools RBAC test:**

These tests cover the RBAC tests of network subnetpools.

Implementation:
`SubnetPoolsRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/network/test_subnetpools_rbac.py>`_

- patrole_tempest_plugin.tests.api.network.test_subnetpools_rbac.SubnetPoolsRbacTest.test_create_subnetpool
- patrole_tempest_plugin.tests.api.network.test_subnetpools_rbac.SubnetPoolsRbacTest.test_create_subnetpool_shared
- patrole_tempest_plugin.tests.api.network.test_subnetpools_rbac.SubnetPoolsRbacTest.test_delete_subnetpool
- patrole_tempest_plugin.tests.api.network.test_subnetpools_rbac.SubnetPoolsRbacTest.test_show_subnetpool
- patrole_tempest_plugin.tests.api.network.test_subnetpools_rbac.SubnetPoolsRbacTest.test_update_subnetpool
- patrole_tempest_plugin.tests.api.network.test_subnetpools_rbac.SubnetPoolsRbacTest.test_update_subnetpool_is_default


**Network subnets RBAC test:**

These tests cover the RBAC tests of network subnets.

Implementation:
`SubnetsRbacTest <https://github.com/openstack/patrole/blob/0.2.0/patrole_tempest_plugin/tests/api/network/test_subnets_rbac.py>`_

- patrole_tempest_plugin.tests.api.network.test_subnets_rbac.SubnetsRbacTest.test_create_subnet
- patrole_tempest_plugin.tests.api.network.test_subnets_rbac.SubnetsRbacTest.test_delete_subnet
- patrole_tempest_plugin.tests.api.network.test_subnets_rbac.SubnetsRbacTest.test_list_subnets
- patrole_tempest_plugin.tests.api.network.test_subnets_rbac.SubnetsRbacTest.test_show_subnet
- patrole_tempest_plugin.tests.api.network.test_subnets_rbac.SubnetsRbacTest.test_update_subnet
