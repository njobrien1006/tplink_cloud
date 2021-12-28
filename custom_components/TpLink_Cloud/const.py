"""Constants for TpLink_Cloud."""
# Base component constants
NAME = "Tp-Link Kasa Cloud"
DOMAIN = "TpLink_Cloud"
DOMAIN_DATA = f"{DOMAIN}_data"
VERSION = "0.0.3"
ATTRIBUTION = "Data provided by https://use1-wap.tplinkcloud.com"
ISSUE_URL = "https://github.com/njobrien1006/tplink_cloud/issues"

# Platforms
SWITCH = "switch"
PLATFORMS = [SWITCH]


# Configuration and options
CONF_ENABLED = "enabled"
CONF_USERNAME = "username"
CONF_PASSWORD = "password"

# Defaults
DEFAULT_NAME = DOMAIN

# Plug Configs
KP400 = {}
KP400 = [
      {
         "alias":"Child 1",
         "id":"00",
         "state":0
      },
      {
         "alias":"Child 2",
         "id":"01",
         "state":0
      }
   ]



STARTUP_MESSAGE = f"""
-------------------------------------------------------------------
{NAME}
Version: {VERSION}
This is a custom integration!
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""
