========================
Installing with Devstack
========================

0. Prepare the Environment::

    sudo mkdir -p /opt/stack
    sudo chown -R ${USER}:$(groups | cut -d ' ' -f 1) /opt/stack
    sudo apt install --yes bridge-utils

1. Download DevStack::

    git clone https://git.openstack.org/openstack-dev/devstack /opt/stack/devstack -b stable/pike
    cd /opt/stack/devstack

2. Modify DevStack's local.conf to pull in both Ceilometer and this
   project by adding in the section ``[[local|localrc]]`` or creating
   the section with::

    [[local|localrc]]
    enable_plugin ceilometer https://git.openstack.org/openstack/ceilometer stable/pike
    enable_plugin ceilometer-fiware https://github.com/SmartInfrastructures/ceilometer-fiware.git stable/pike

3. See TODO then configure the installation through options in
   local.conf as needed.

4. Run ``stack.sh`` from devstack::

    cd /opt/stack/devstack
    ./stack.sh
