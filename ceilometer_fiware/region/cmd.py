from __future__ import print_function


def main():
    """Entry point for CLI to run the Region Pollster"""
    try:
        from ceilometer_fiware.region.region import RegionPollster
        rp = RegionPollster(None)
        for i, sample in enumerate(rp.get_samples(None, None, None)):
            print("Sample #{}: {}".format(i, sample))
    except Exception as exc:
        print(exc)
