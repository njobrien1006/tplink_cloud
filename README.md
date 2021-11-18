# TP-Link Kasa Clound Integration

Integration to communicate and change the state of Kasa Cloud Devices. Mostly intended for use with Outlet Plugs as we are using assumed state in conjunction with periodic Cloud Polling. Explicitly not intended to poll Kasa's Cloud for LightSwitch changes. 

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]

[![Discord][discord-shield]][discord]
[![Community Forum][forum-shield]][forum]

_Component to integrate with [integration_api][Tp-Link Kasa]._

**This component will set up the following platforms.**

Platform | Description
-- | --
`switch` | Switch For Plugs `True` or `False`.

![Device1][Device1img]

## Installation

	@@ -33,16 +29,10 @@ Platform | Description

Using your HA configuration directory (folder) as a starting point you should now also have this:

```text
custom_components/integration_blueprint/translations/en.json
custom_components/integration_blueprint/__init__.py
custom_components/integration_blueprint/tplinkcloud.py
custom_components/integration_blueprint/binary_sensor.py
custom_components/integration_blueprint/config_flow.py
custom_components/integration_blueprint/const.py
custom_components/integration_blueprint/manifest.json
custom_components/integration_blueprint/switch.py
```

## Configuration is done in the UI

<!---->
## Contributions are welcome!
If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)
***
[integration_blueprint]: https://github.com/njobrien1006/tplink_cloud
[integration_api]: https://www.kasasmart.com
[commits-shield]: https://img.shields.io/github/commit-activity/y/custom-components/blueprint.svg?style=for-the-badge
[commits]: https://github.com/njobrien1006/tplink_cloud/commit/master
[hacs]: https://github.com/custom-components/hacs
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[discord]: https://discord.gg/Qa5fW2R
[discord-shield]: https://img.shields.io/discord/330944238910963714.svg?style=for-the-badge
[Device1img]: Device1.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/custom-components/blueprint.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/custom-components/blueprint.svg?style=for-the-badge
[releases]: https://github.com/njobrien1006/tplink_cloud/releases
