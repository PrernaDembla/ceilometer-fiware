FIWARE Lab monitoring system Ceilometer Plugin
==============================================

Installation
------------

Configure Ceilometer
++++++++++++++++++++

Configure Ceilometer in one controller where the service
=ceilometer-agent-central= is running.

In =/etc/ceilometer/ceilometer.conf= and add these entries (with your
current values).

Pay attention to the `netlist` attribute: the names of external
networks in your OpenStack installation.::

    [region]
    latitude=1.1
    longitude=12.2
    location=IT
    netlist=net04_ext,net05_ext
    ram_allocation_ratio=1.5
    cpu_allocation_ratio=16

Install the plugin
++++++++++++++++++

Install the plugin, for example using pip::

    pip install git+https://github.com/SmartInfrastructures/ceilometer-fiware.git@stable/pike#egg=ceilometer-fiware

Check the pollster
++++++++++++++++++

Check if everything is configured properly by running::

    pollster_test_fiware_region
    pollster_test_fiware_host

You should see a debug output.  If everything is correct you should
spot something like the following in the output::

    Publish sample: <name: region.used_ip, volume: 0, resource_id: RegionOne, timestamp: 2018-06-08T12:00:00Z>

Restart the service
+++++++++++++++++++

Restart the Ceilometer Central Agent service, usually under
`systemd`::

    service ceilometer-agent-central restart

Continue the setup
++++++++++++++++++

For additional configuration of the monitoring pipeline see the guide
at:
https://github.com/SmartInfrastructures/ceilometer-plugin-fiware#monasca
