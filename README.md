# HomeAssistant Carrier Infinity

HomeAssistant plugin for Carrier Infinity / Bryant Evolution / ICP Brands Ion thermostats.

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]

_Component to integrate with [integration_api][Tp-Link Kasa]._

# Supported Systems

This is a standalone plugin for Homebridge that talks directly to the Infinity/Evolution/Ion api. It should support these similar systems:
* [Carrier Infinity](https://www.myinfinitytouch.carrier.com/Account/Register)</a>
* [Bryant Evolution](https://www.myevolutionconnex.bryant.com/Account/Register)</a>
* [ICP Brands Ion](https://www.ioncomfort.com/Account/Register) (including Airquest, Arcoaire, Comfortmaker, Day&Night, Heil, Keeprite, Tempstar)

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
2. If you do not have a `custom_components` directory (folder) there, you need to create it.
3. In the `custom_components` directory (folder) create a new folder called `TpLink_Cloud`.
4. Download _all_ the files from the `custom_components/TpLink_Cloud/` directory (folder) in this repository.
5. Place the files you downloaded in the new directory (folder) you created.
6. Restart Home Assistant
7. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Tp-Link"

Using your HA configuration directory (folder) as a starting point you should now also have this:

# Notes

* It may take 1-2 minutes from the time you make a change via HomeKit until your thermostat sees the change. This is an unavoidable result of how the thermostats poll for updates.
* This plugin *does not* require Infinitude/Infinitive.

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
