#
# Copyright 2015 CREATE-NET <abroglio AT create-net DOT org>
#
#
# Version: 1.2.0
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from oslo_log import log
from ceilometer.agent import plugin_base
from ceilometer.i18n import _
from ceilometer import sample
from oslo_utils import timeutils
from oslo_config import cfg
from novaclient import client
from keystoneauth1 import identity
from keystoneauth1 import session
from ceilometer.keystone_client import get_session

LOG = log.getLogger(__name__)

from ceilometer import service
from ceilometer.cmd.polling import CLI_OPTS
conf = cfg.ConfigOpts()
conf.register_cli_opts(CLI_OPTS)
conf2 = service.prepare_service(conf=conf)

sess = get_session(conf2)

class HostPollster(plugin_base.PollsterBase):

    @property
    def default_discovery(self):
        return 'host'

    @staticmethod
    def get_samples(manager, cache, resources):
        nt = client.Client(version='2', session=sess)

        for host in resources:
            LOG.debug(_('checking host %s'), host)
            try:
                info = nt.hosts.get(host)
                values = []
                if len(info) >= 3:
                    # total
                    values.append({'name': 'ram.tot', 'unit': 'MB', 'value': (
                        info[0].memory_mb if info[0].memory_mb else 0)})
                    values.append({'name': 'disk.tot', 'unit': 'GB', 'value': (
                        info[0].disk_gb if info[0].disk_gb else 0)})
                    values.append({'name': 'cpu.tot', 'unit': 'cpu',
                                   'value': (info[0].cpu if info[0].cpu else 0)})
                    # now
                    values.append({'name': 'ram.now', 'unit': 'MB', 'value': (
                        info[1].memory_mb if info[1].memory_mb else 0)})
                    values.append({'name': 'disk.now', 'unit': 'GB', 'value': (
                        info[1].disk_gb if info[1].disk_gb else 0)})
                    values.append({'name': 'cpu.now', 'unit': 'cpu',
                                   'value': (info[1].cpu if info[1].cpu else 0)})
                    # max
                    values.append({'name': 'ram.max', 'unit': 'MB', 'value': (
                        info[2].memory_mb if info[2].memory_mb else 0)})
                    values.append({'name': 'disk.max', 'unit': 'GB', 'value': (
                        info[2].disk_gb if info[2].disk_gb else 0)})
                    values.append({'name': 'cpu.max', 'unit': 'cpu',
                                   'value': (info[2].cpu if info[2].cpu else 0)})

                for item in values:
                    my_sample = sample.Sample(
                        name="compute.node.%s" % item['name'],
                        type=sample.TYPE_GAUGE,
                        unit=item['unit'],
                        volume=item['value'],
                        user_id=None,
                        project_id=None,
                        resource_id="%s_%s" % (host, host),
                        timestamp=timeutils.isotime(),
                        resource_metadata={}
                    )
                    LOG.debug("Publish sample: %s" % (my_sample))
                    yield my_sample

            except Exception as err:
                LOG.exception(_('could not get info for host %(host)s: %(e)s'), {
                              'host': host, 'e': err})
