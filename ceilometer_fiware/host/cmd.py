from __future__ import print_function


def main():
    """Entry point for CLI to run the Host Pollster"""
    try:
        from ceilometer_fiware.host.discovery import HostDiscovery
        from ceilometer_fiware.host.host import HostPollster
        rp = HostPollster(None)
        hostd = HostDiscovery(None)
        resources = hostd.discover(None)
        for i, sample in enumerate(rp.get_samples(None, None, resources)):
            print("Sample #{}: {}".format(i, sample))
    except Exception as exc:
        print(exc)
