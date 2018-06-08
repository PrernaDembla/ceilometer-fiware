from oslo_log import log
from ceilometer.agent import plugin_base as plugin

LOG = log.getLogger(__name__)

LOG.debug('Loading module')

class RegionDiscovery(plugin.DiscoveryBase):
    def discover(self, manager, param=None):
        LOG.debug('Entering method')
        # TODO: find a more suitable value
        return ['region']
