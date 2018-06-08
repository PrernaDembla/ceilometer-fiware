#!/bin/bash

# Devstack extras script to install and configure the ceilometer for
# ceilometer-fiware

# The following entry points are called in this order for
# ceilometer-fiware:
#
# - install_ceilometer_fiware
# - configure_ceilometer_fiware
# - start_ceilometer_fiware
# - stop_ceilometer_fiware
# - cleanup_ceilometer_fiware

# Save trace setting
MY_XTRACE=$(set +o | grep xtrace)
set +o xtrace

set -x

# Defaults
# --------

# Set up base directories
CEILOMETER_CONF_DIR=${CEILOMETER_CONF_DIR:-/etc/ceilometer}
CEILOMETER_CONF=${CEILOMETER_CONF:-CEILOMETER_CONF_DIR/ceilometer.conf}

# ceilometer-fiware directories
CEILOMETER_FIWARE_REGION_DIR=${CEILOMETER_FIWARE_REGION_DIR:-${DEST}/ceilometer-fiware}
CEILOMETER_FIWARE_REGION_PLUGIN_DIR=$(readlink -f $(dirname ${BASH_SOURCE[0]}))

# Entry Points
# ------------

# Configure the system to use ceilometer_fiware
function configure_ceilometer_fiware {
    # TODO: etc config should be done here?
    cp -v -f "${CEILOMETER_FIWARE_REGION_DIR}/etc/ceilometer/polling.yaml" "${CEILOMETER_CONF_DIR}/fiware_debug"
}

# Install ceilometer_fiware and necessary dependencies
function install_ceilometer_fiware {
    # Install the ceilometer-fiware package
    setup_develop $CEILOMETER_FIWARE_REGION_DIR
}

# Start the ceilometer_fiware process
function start_ceilometer_fiware {
    # TODO: etc config should be done here?
    run_process ceilometer-fiware "$CEILOMETER_BIN_DIR/ceilometer-polling --polling-namespaces central --config-file $CEILOMETER_CONF fiware_debug"
}

# Stop the ceilometer_fiware process
function stop_ceilometer_fiware {
    # Stop the pvm ceilometer compute agent
    stop_process ceilometer-fiware
}

# Cleanup the ceilometer_fiware process
function cleanup_ceilometer_fiware {
    # This function intentionally left blank
    :
}

# Core Dispatch
# -------------
if is_service_enabled ceilometer_fiware; then
    if [[ "$1" == "stack" && "$2" == "pre-install" ]]; then
        echo_summary "Installing Ceilometer Fiware Region"
        install_ceilometer_fiware
    fi

    if [[ "$1" == "stack" && "$2" == "install" ]]; then
        # Perform installation of ceilometer-fiware
        echo_summary "Installing ceilometer-fiware"
        install_ceilometer_fiware

    elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
        # Lay down configuration post install
        echo_summary "Configuring ceilometer-fiware"
        configure_ceilometer_fiware

    elif [[ "$1" == "stack" && "$2" == "extra" ]]; then
        # Initialize and start the ceilometer compute agent for Fiware_Region
        echo_summary "Starting ceilometer-fiware"
        start_ceilometer_fiware
    fi

    if [[ "$1" == "unstack" ]]; then
        # Shut down the ceilometer compute agent for Fiware_Region
        echo_summary "Stopping ceilometer-fiware"
        stop_ceilometer_fiware
    fi

    if [[ "$1" == "clean" ]]; then
        # Remove any lingering configuration data
        # clean.sh first calls unstack.sh
        echo_summary "Cleaning up ceilometer-fiware and associated data"
        cleanup_ceilometer_fiware
    fi
fi

set +x

# Restore xtrace
$MY_XTRACE

# Local variables:
# mode: shell-script
# End:
