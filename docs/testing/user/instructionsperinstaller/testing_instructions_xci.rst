.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Technologies Co.,Ltd and others.

===========================================================
Conducting OVP Testing with Dovetail using XCI installer
===========================================================

Overview
------------------------------
The purpose of this document is to give tips for the dovetail deployment
on XCI installer.
The general structure of the document is remaining according to the user guide
document and the XCI related tips will be added under of the respective
chapter's name.

In order to deploy properly the XCI installer the below steps should be followed:

1- The prerequisites of chapter 2.4.1 of XCI User Guide [1] should be applied.

2- If you don’t have one already, generate an SSH key in $HOME/.ssh
   ssh-keygen -t rsa

3- Clone OPNFV releng-xci repository

4- Change into directory where the sandbox script is located:
   cd releng-xci/xci

5- Set the sandbox flavor, OPNFV scenario, openstack version, VM size and releng_xci and bifrost versions:

   export INSTALLER_TYPE=osa
   export XCI_FLAVOR=xxx ,chapter 2.3 of XCI User Guide [1]
   (e.g. export XCI_FLAVOR=mini)
   export DEPLOY_SCENARIO=yyy
   (e.g. export DEPLOY_SCENARIO=os-nosdn-nofeature)

6- Execute the sandbox script
   ./xci-deploy.sh

Once the deployement is successfully completed, the instructions below should be completed:

1- You should access the OPNFV VM using ssh (ssh root@192.168.122.2)

2- export DEPLOY_SCENARIO=yyy

3- export PDF=/root/releng-xci/xci/var/pdf.yml
   export IDF=/root/releng-xci/xci/var/idf.yml
   source openrc

4- Run the following ansible playbook script:
   ansible-playbook -i releng-xci/xci/playbooks/dynamic_inventory.py releng-xci/xci/playbooks/prepare-tests.yml

5- Run the following bash script:
   ./prepare-tests.sh



[1] https://docs.opnfv.org/en/latest/infrastructure/xci.html


Installing Dovetail
--------------------


Checking the Test Host Readiness
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Installing Prerequisite Packages on the Test Host
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Configuring the Test Host Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to run the test scenarios properly and having access to all OS components
that each scenario needs, the undercloud credentials should be used and copied in the
docker container along with ssh key.

The environment preparation should be applied on the Test Host environment.
Therefore, the containers which are going to be used as part of this configuration,
fetch the information, the files and the rest input from Test Host environment directly
as part of the Docker command.

Setting up Primary Configuration File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Two new environment variables could be introduced in the ``env_config.sh`` file.


.. code-block:: bash

   # For XCI installer the following environment parameters should be added in
   # this file. Otherwise, those parameters could be ignored.
   export INSTALLER_TYPE=osa
   export DEPLOY_SCENARIO=os-nosdn-nofeature
   export XCI_FLAVOR=noha

The OS_PASSWORD and the rest credential details could be retrieved directly by openrc file in the OPNFV VM.

Configuration for Running Tempest Test Cases (Mandatory)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Configuration for Running HA Test Cases (Mandatory)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Below is a sample of ``${DOVETAIL_HOME}/pre_config/pod.yaml`` file with
the required syntax when key_filename is used instead of password is employed
by the controller.
Moreover, the 'heat-admin' should be used as user.

.. code-block:: bash

   nodes:
   -
       # This can not be changed and must be node0.
       name: node0

       # This must be Jumpserver.
       role: Jumpserver

       # This is the instance IP of a node which has ipmitool installed.
       ip: xx.xx.xx.xx

       # User name of the user of this node. This user **must** have sudo privileges.
       user: root

       # Password of the user.
       #password: root
       key_filename: /root/.ssh/id_rsa

   -
       # This can not be changed and must be node1.
       name: node1

       # This must be controller.
       role: Controller

       # This is the instance IP of a controller node, which is the haproxy primary node
       ip: xx.xx.xx.xx

       # User name of the user of this node. This user **must** have sudo privileges.
       user: root

       # Password of the user.
       #password: root
       key_filename: /root/.ssh/id_rsa

   -
       # This can not be changed and must be node2.
       name: node2

       # This must be Compute.
       role: Compute

       # This is the instance IP of a controller node, which is the haproxy primary node
       ip: xx.xx.xx.xx

       # User name of the user of this node. This user **must** have sudo privileges.
       user: root

       # Password of the user.
       #password: root
       key_filename: /root/.ssh/id_rsa

   process_info:
   -
       # The default attack process of yardstick.ha.rabbitmq is 'rabbitmq-server'.
       # Here can be reset to 'rabbitmq'.
       testcase_name: yardstick.ha.rabbitmq
       attack_process: rabbitmq

   -
       # The default attack host for all HA test cases is 'node1'.
       # Here can be reset to any other node given in the section 'nodes'.
       testcase_name: yardstick.ha.glance_api
       attack_host: node2

Note: The definition for each active controller and computer should be done in this file.

Configuration of Hosts File (Optional)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Installing Dovetail on the Test Host
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Online Test Host
""""""""""""""""


Offline Test Host
"""""""""""""""""


Starting Dovetail Docker
------------------------


Running the OVP Test Suite
----------------------------


Making Sense of OVP Test Results
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


OVP Portal Web Interface
------------------------


Updating Dovetail or a Test Suite
---------------------------------
