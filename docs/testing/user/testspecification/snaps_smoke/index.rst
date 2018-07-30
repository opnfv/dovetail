.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) Ericsson AB

==============================
SNAPS smoke test specification
==============================

.. toctree::
   :maxdepth: 2

Scope
=====

The SNAPS smoke test case contains tests that setup and destroy environments
with VMs with and without Floating IPs with a newly created user and project.

References
==========

This smoke test executes the Python Tests included with the SNAPS libraries
that exercise many of the OpenStack APIs within Keystone, Glance, Neutron,
and Nova.

- https://wiki.opnfv.org/display/PROJ/SNAPS-OO

System Under Test (SUT)
=======================

The SUT is assumed to be the NFVi and VIM in operation on a Pharos compliant infrastructure.


Test Area Structure
===================

The test area is structured in individual tests as listed below.
For detailed information on the individual steps and assertions performed
by the tests, review the Python source code accessible via the following links:

**Dynamic creation of User/Project objects to be leveraged for the integration tests:**

- `Create Image Success tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_image_tests.py#L254>`_
    - snaps.openstack.tests.create_image_tests.CreateImageSuccessTests.test_create_delete_image
    - snaps.openstack.tests.create_image_tests.CreateImageSuccessTests.test_create_image_clean_file
    - snaps.openstack.tests.create_image_tests.CreateImageSuccessTests.test_create_image_clean_url
    - snaps.openstack.tests.create_image_tests.CreateImageSuccessTests.test_create_image_clean_url_properties
    - snaps.openstack.tests.create_image_tests.CreateImageSuccessTests.test_create_same_image
    - snaps.openstack.tests.create_image_tests.CreateImageSuccessTests.test_create_same_image_new_settings

- `Create Image Negative tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_image_tests.py#L463>`_
    - snaps.openstack.tests.create_image_tests.CreateImageNegativeTests.test_bad_image_file
    - snaps.openstack.tests.create_image_tests.CreateImageNegativeTests.test_bad_image_image_type
    - snaps.openstack.tests.create_image_tests.CreateImageNegativeTests.test_bad_image_name
    - snaps.openstack.tests.create_image_tests.CreateImageNegativeTests.test_bad_image_url

- `Create Image Multi Part tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_image_tests.py#L551>`_
    - snaps.openstack.tests.create_image_tests.CreateMultiPartImageTests.test_create_three_part_image_from_file_3_creators
    - snaps.openstack.tests.create_image_tests.CreateMultiPartImageTests.test_create_three_part_image_from_url
    - snaps.openstack.tests.create_image_tests.CreateMultiPartImageTests.test_create_three_part_image_from_url_3_creators

- `Create Keypairs tests <https://github.com/opnfv/snaps/blob/stable%2Ffraser/snaps/openstack/tests/create_keypairs_tests.py#L192>`_
    - snaps.openstack.tests.create_keypairs_tests.CreateKeypairsTests.test_create_delete_keypair
    - snaps.openstack.tests.create_keypairs_tests.CreateKeypairsTests.test_create_keypair_from_file
    - snaps.openstack.tests.create_keypairs_tests.CreateKeypairsTests.test_create_keypair_large_key
    - snaps.openstack.tests.create_keypairs_tests.CreateKeypairsTests.test_create_keypair_only
    - snaps.openstack.tests.create_keypairs_tests.CreateKeypairsTests.test_create_keypair_save_both
    - snaps.openstack.tests.create_keypairs_tests.CreateKeypairsTests.test_create_keypair_save_pub_only

- `Create Keypairs Cleanup tests <https://github.com/opnfv/snaps/blob/stable%2Ffraser/snaps/openstack/tests/create_keypairs_tests.py#L361>`_
    - snaps.openstack.tests.create_keypairs_tests.CreateKeypairsCleanupTests.test_create_keypair_exist_files_delete
    - snaps.openstack.tests.create_keypairs_tests.CreateKeypairsCleanupTests.test_create_keypair_exist_files_keep
    - snaps.openstack.tests.create_keypairs_tests.CreateKeypairsCleanupTests.test_create_keypair_gen_files_delete_1
    - snaps.openstack.tests.create_keypairs_tests.CreateKeypairsCleanupTests.test_create_keypair_gen_files_delete_2
    - snaps.openstack.tests.create_keypairs_tests.CreateKeypairsCleanupTests.test_create_keypair_gen_files_keep

- `Create Network Success tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_network_tests.py#L355>`_
    - snaps.openstack.tests.create_network_tests.CreateNetworkSuccessTests.test_create_delete_network
    - snaps.openstack.tests.create_network_tests.CreateNetworkSuccessTests.test_create_network_router_admin_user_to_new_project
    - snaps.openstack.tests.create_network_tests.CreateNetworkSuccessTests.test_create_network_router_new_user_to_admin_project
    - snaps.openstack.tests.create_network_tests.CreateNetworkSuccessTests.test_create_network_with_router
    - snaps.openstack.tests.create_network_tests.CreateNetworkSuccessTests.test_create_network_without_router
    - snaps.openstack.tests.create_network_tests.CreateNetworkSuccessTests.test_create_networks_same_name

- `Create Router Success tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_router_tests.py#L118>`_
    - snaps.openstack.tests.create_router_tests.CreateRouterSuccessTests.test_create_delete_router
    - snaps.openstack.tests.create_router_tests.CreateRouterSuccessTests.test_create_router_admin_state_True
    - snaps.openstack.tests.create_router_tests.CreateRouterSuccessTests.test_create_router_admin_state_false
    - snaps.openstack.tests.create_router_tests.CreateRouterSuccessTests.test_create_router_admin_user_to_new_project
    - snaps.openstack.tests.create_router_tests.CreateRouterSuccessTests.test_create_router_external_network
    - snaps.openstack.tests.create_router_tests.CreateRouterSuccessTests.test_create_router_new_user_as_admin_project
    - snaps.openstack.tests.create_router_tests.CreateRouterSuccessTests.test_create_router_private_network
    - snaps.openstack.tests.create_router_tests.CreateRouterSuccessTests.test_create_router_vanilla
    - snaps.openstack.tests.create_router_tests.CreateRouterSuccessTests.test_create_router_with_ext_port
    - snaps.openstack.tests.create_router_tests.CreateRouterSuccessTests.test_create_with_internal_sub
    - snaps.openstack.tests.create_router_tests.CreateRouterSuccessTests.test_create_with_invalid_internal_sub

- `Create Router Negative tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_router_tests.py#L514>`_
    - snaps.openstack.tests.create_router_tests.CreateRouterNegativeTests.test_create_router_admin_ports
    - snaps.openstack.tests.create_router_tests.CreateRouterNegativeTests.test_create_router_invalid_gateway_name
    - snaps.openstack.tests.create_router_tests.CreateRouterNegativeTests.test_create_router_noname


- `Create QoS tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_qos_tests.py#L112>`_
    - snaps.openstack.tests.create_qos_tests.CreateQoSTests.test_create_delete_qos
    - snaps.openstack.tests.create_qos_tests.CreateQoSTests.test_create_qos
    - snaps.openstack.tests.create_qos_tests.CreateQoSTests.test_create_same_qos

- `Create Simple Volume Success tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_volume_tests.py#L116>`_
    - snaps.openstack.tests.create_volume_tests.CreateSimpleVolumeSuccessTests.test_create_delete_volume
    - snaps.openstack.tests.create_volume_tests.CreateSimpleVolumeSuccessTests.test_create_same_volume
    - snaps.openstack.tests.create_volume_tests.CreateSimpleVolumeSuccessTests.test_create_volume_simple

- `Create Simple Volume Failure tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_volume_tests.py#L116>`_
    - snaps.openstack.tests.create_volume_tests.CreateSimpleVolumeFailureTests.test_create_volume_bad_image
    - snaps.openstack.tests.create_volume_tests.CreateSimpleVolumeFailureTests.test_create_volume_bad_size
    - snaps.openstack.tests.create_volume_tests.CreateSimpleVolumeFailureTests.test_create_volume_bad_type

- `Create Volume With Type tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_volume_tests.py#L286>`_
    - snaps.openstack.tests.create_volume_tests.CreateVolumeWithTypeTests.test_bad_volume_type
    - snaps.openstack.tests.create_volume_tests.CreateVolumeWithTypeTests.test_valid_volume_type

- `Create Volume With Image tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_volume_tests.py#L336>`_
    - snaps.openstack.tests.create_volume_tests.CreateVolumeWithImageTests.test_bad_image_name
    - snaps.openstack.tests.create_volume_tests.CreateVolumeWithImageTests.test_valid_volume_image

- `Create Simple Volume Type Success tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_volume_type_tests.py#L113>`_
    - snaps.openstack.tests.create_volume_type_tests.CreateSimpleVolumeTypeSuccessTests.test_create_delete_volume_type
    - snaps.openstack.tests.create_volume_type_tests.CreateSimpleVolumeTypeSuccessTests.test_create_same_volume_type
    - snaps.openstack.tests.create_volume_type_tests.CreateSimpleVolumeTypeSuccessTests.test_create_volume_type

- `Create Volume Type Complex tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_volume_type_tests.py#L206>`_
    - snaps.openstack.tests.create_volume_type_tests.CreateVolumeTypeComplexTests.test_volume_type_with_encryption
    - snaps.openstack.tests.create_volume_type_tests.CreateVolumeTypeComplexTests.test_volume_type_with_qos
    - snaps.openstack.tests.create_volume_type_tests.CreateVolumeTypeComplexTests.test_volume_type_with_qos_and_encryption

- `Simple Health Check <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_instance_tests.py#L283>`_
    - snaps.openstack.tests.create_instance_tests.SimpleHealthCheck.test_check_vm_ip_dhcp

- `Create Instance Two Net tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_instance_tests.py#L2835>`_
    - snaps.openstack.tests.create_instance_tests.CreateInstanceTwoNetTests.test_ping_via_router

- `Create Instance Simple tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_instance_tests.py#L408>`_
    - snaps.openstack.tests.create_instance_tests.CreateInstanceSimpleTests.test_create_admin_instance
    - snaps.openstack.tests.create_instance_tests.CreateInstanceSimpleTests.test_create_delete_instance

- `Create Instance Port Manipulation tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_instance_tests.py#L1343>`_
    - snaps.openstack.tests.create_instance_tests.CreateInstancePortManipulationTests.test_set_allowed_address_pairs
    - snaps.openstack.tests.create_instance_tests.CreateInstancePortManipulationTests.test_set_allowed_address_pairs_bad_ip
    - snaps.openstack.tests.create_instance_tests.CreateInstancePortManipulationTests.test_set_allowed_address_pairs_bad_mac
    - snaps.openstack.tests.create_instance_tests.CreateInstancePortManipulationTests.test_set_custom_invalid_ip_one_subnet
    - snaps.openstack.tests.create_instance_tests.CreateInstancePortManipulationTests.test_set_custom_invalid_mac
    - snaps.openstack.tests.create_instance_tests.CreateInstancePortManipulationTests.test_set_custom_mac_and_ip
    - snaps.openstack.tests.create_instance_tests.CreateInstancePortManipulationTests.test_set_custom_valid_ip_one_subnet
    - snaps.openstack.tests.create_instance_tests.CreateInstancePortManipulationTests.test_set_custom_valid_mac
    - snaps.openstack.tests.create_instance_tests.CreateInstancePortManipulationTests.test_set_one_port_two_ip_one_subnet
    - snaps.openstack.tests.create_instance_tests.CreateInstancePortManipulationTests.test_set_one_port_two_ip_two_subnets

- `Instance Security Group tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_instance_tests.py#L283>`_
    - snaps.openstack.tests.create_instance_tests.InstanceSecurityGroupTests.test_add_invalid_security_group
    - snaps.openstack.tests.create_instance_tests.InstanceSecurityGroupTests.test_add_same_security_group
    - snaps.openstack.tests.create_instance_tests.InstanceSecurityGroupTests.test_add_security_group
    - snaps.openstack.tests.create_instance_tests.InstanceSecurityGroupTests.test_remove_security_group
    - snaps.openstack.tests.create_instance_tests.InstanceSecurityGroupTests.test_remove_security_group_never_added

- `Create Instance On Compute Host <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_instance_tests.py#L1738>`_
    - snaps.openstack.tests.create_instance_tests.CreateInstanceOnComputeHost.test_deploy_vm_to_each_compute_node

- `Create Instance From Three Part Image <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_instance_tests.py#L2205>`_
    - snaps.openstack.tests.create_instance_tests.CreateInstanceFromThreePartImage.test_create_instance_from_three_part_image

- `Create Instance Volume tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_instance_tests.py#L3062>`_
    - snaps.openstack.tests.create_instance_tests.CreateInstanceVolumeTests.test_create_instance_with_one_volume
    - snaps.openstack.tests.create_instance_tests.CreateInstanceVolumeTests.test_create_instance_with_two_volumes

- `Create Instance Single Network tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_instance_tests.py#L687>`_
    - snaps.openstack.tests.create_instance_tests.CreateInstanceSingleNetworkTests.test_single_port_static
    - snaps.openstack.tests.create_instance_tests.CreateInstanceSingleNetworkTests.test_ssh_client_fip_after_active
    - snaps.openstack.tests.create_instance_tests.CreateInstanceSingleNetworkTests.test_ssh_client_fip_after_init
    - snaps.openstack.tests.create_instance_tests.CreateInstanceSingleNetworkTests.test_ssh_client_fip_after_reboot
    - snaps.openstack.tests.create_instance_tests.CreateInstanceSingleNetworkTests.test_ssh_client_fip_before_active
    - snaps.openstack.tests.create_instance_tests.CreateInstanceSingleNetworkTests.test_ssh_client_fip_reverse_engineer
    - snaps.openstack.tests.create_instance_tests.CreateInstanceSingleNetworkTests.test_ssh_client_fip_second_creator


- `Create Stack Success tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_stack_tests.py#L131>`_
    - snaps.openstack.tests.create_stack_tests.CreateStackSuccessTests.test_create_delete_stack
    - snaps.openstack.tests.create_stack_tests.CreateStackSuccessTests.test_create_same_stack
    - snaps.openstack.tests.create_stack_tests.CreateStackSuccessTests.test_create_stack_short_timeout
    - snaps.openstack.tests.create_stack_tests.CreateStackSuccessTests.test_create_stack_template_dict
    - snaps.openstack.tests.create_stack_tests.CreateStackSuccessTests.test_create_stack_template_file
    - snaps.openstack.tests.create_stack_tests.CreateStackSuccessTests.test_retrieve_network_creators
    - snaps.openstack.tests.create_stack_tests.CreateStackSuccessTests.test_retrieve_vm_inst_creators

- `Create Stack Volume tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_stack_tests.py#L735>`_
    - snaps.openstack.tests.create_stack_tests.CreateStackVolumeTests.test_retrieve_volume_creator
    - snaps.openstack.tests.create_stack_tests.CreateStackVolumeTests.test_retrieve_volume_type_creator

- `Create Stack Flavor tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_stack_tests.py#L829>`_
    - snaps.openstack.tests.create_stack_tests.CreateStackFlavorTests.test_retrieve_flavor_creator

- `Create Stack Keypair tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_stack_tests.py#L888>`_
    - snaps.openstack.tests.create_stack_tests.CreateStackKeypairTests.test_retrieve_keypair_creator

- `Create Stack Security Group tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_stack_tests.py#L969>`_
    - snaps.openstack.tests.create_stack_tests.CreateStackSecurityGroupTests.test_retrieve_security_group_creatorl

- `Create Stack Negative tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_stack_tests.py#L1062>`_
    - snaps.openstack.tests.create_stack_tests.CreateStackNegativeTests.test_bad_stack_file
    - snaps.openstack.tests.create_stack_tests.CreateStackNegativeTest.test_missing_dependencies

- `Create Security Group tests <https://github.com/opnfv/snaps/blob/stable%2Ffraser/snaps/openstack/tests/create_security_group_tests.py#L199>`_
    - snaps.openstack.tests.create_security_group_tests.CreateSecurityGroupTests.test_add_rule
    - snaps.openstack.tests.create_security_group_tests.CreateSecurityGroupTests.test_create_delete_group
    - snaps.openstack.tests.create_security_group_tests.CreateSecurityGroupTests.test_create_group_admin_user_to_new_project
    - snaps.openstack.tests.create_security_group_tests.CreateSecurityGroupTests.test_create_group_new_user_to_admin_project
    - snaps.openstack.tests.create_security_group_tests.CreateSecurityGroupTests.test_create_group_with_one_complex_rule
    - snaps.openstack.tests.create_security_group_tests.CreateSecurityGroupTests.test_create_group_with_one_simple_rule
    - snaps.openstack.tests.create_security_group_tests.CreateSecurityGroupTests.test_create_group_with_several_rules
    - snaps.openstack.tests.create_security_group_tests.CreateSecurityGroupTests.test_create_group_without_rules
    - snaps.openstack.tests.create_security_group_tests.CreateSecurityGroupTests.test_remove_rule_by_id
    - snaps.openstack.tests.create_security_group_tests.CreateSecurityGroupTests.test_remove_rule_by_setting

**Floating IP and Ansible provisioning:**

- `Create Stack Floating tests <https://github.com/opnfv/snaps/blob/stable/fraser/snaps/openstack/tests/create_stack_tests.py#L414>`_
    - snaps.openstack.tests.create_stack_tests.CreateStackFloatingIpTests.test_connect_via_ssh_heat_vm
    - snaps.openstack.tests.create_stack_tests.CreateStackFloatingIpTests.test_connect_via_ssh_heat_vm_derived


- `Ansible Provisioning tests <https://github.com/opnfv/snaps/blob/stable%2Ffraser/snaps/provisioning/tests/ansible_utils_tests.py#L48>`_
    - snaps.provisioning.tests.ansible_utils_tests.AnsibleProvisioningTests.test_apply_simple_playbook
    - snaps.provisioning.tests.ansible_utils_tests.AnsibleProvisioningTests.test_apply_template_playbook
