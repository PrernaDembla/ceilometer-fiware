from novaclient import client as nova_client
from oslo_config import cfg

from ceilometer.agent import plugin_base
from ceilometer import keystone_client

from oslo_log import log


LOG = log.getLogger(__name__)

LOG.debug('Loading module')


class _BaseDiscovery(plugin_base.DiscoveryBase):
    def __init__(self, conf):
        super(_BaseDiscovery, self).__init__(conf)


        # TODO: check if we can skip this loading of cfg
        from ceilometer import service
        from ceilometer.cmd.polling import CLI_OPTS
        conf = cfg.ConfigOpts()
        conf.register_cli_opts(CLI_OPTS)
        conf = service.prepare_service(conf=conf)

        creds = conf.service_credentials
        self.client = nova_client.Client(
            version='2',
            session=keystone_client.get_session(conf),
        )

class HostDiscovery(_BaseDiscovery):
    def discover(self, manager, param=None):
        """Discover host resources to monitor."""
        LOG.debug('Entering method')
        # Seems that hosts are duplicated, reduce to a set with names
        hosts_all = self.client.hosts.list_all()
        hosts_uniq = set([host.host_name for host in hosts_all])
        return hosts_uniq
