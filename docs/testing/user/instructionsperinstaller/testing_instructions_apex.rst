.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. http://creativecommons.org/licenses/by/4.0
.. (c) OPNFV, Huawei Technologies Co.,Ltd and others.

===========================================================
Conducting OVP Testing with Dovetail using APEX installer
===========================================================

Overview
------------------------------
The purpose of this document is to give tips for the dovetail deployment
on APEX installer.
The general structure of the document is remaining according to the user guide
document and the APEX related tips will be added under of the respective
chapter's name.


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

   # Set the name of the installer type as environment variable (e.g. apex, fuel, etc)
   # Optional parameter
   export INSTALLER_TYPE=xxxx

   # Set the deployed scenario name (e.g. os-sdn-nofeature-noha)
   # Optional parameter
   export DEPLOY_SCENARIO=xxxx

For the OS_PASSWORD, OpenStack password from undercloud environment should be used.


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
       user: heat-admin

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
       user: heat-admin

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

In case the 'key_filename' method has been chosen as authentication method in the pod.yaml file,
confirm that the ssh key files have been copied in the dovetail container properly
before running the test suite.

Running the OVP Test Suite
----------------------------


Making Sense of OVP Test Results
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


OVP Portal Web Interface
------------------------


Updating Dovetail or a Test Suite
---------------------------------
