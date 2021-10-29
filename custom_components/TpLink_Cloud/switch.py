"""Switch platform for TpLink_Cloud."""
import logging

from homeassistant.components.switch import SwitchEntity

from .const import DEFAULT_NAME, DOMAIN, SWITCH
from .entity import TpLink_CloudEntity
from .tplinkcloud import IntegrationBlueprintApiClient

_LOGGER: logging.Logger = logging.getLogger(__package__)

async def async_setup_entry(hass, entry, async_add_devices):
    """Setup sensor platform."""
    client = hass.data[DOMAIN][entry.entry_id]
    deviceslst = await client.async_rtn_devices()
    await client.async_get_data()
    #_LOGGER.debug(f"DevicesLst: {deviceslst}")
    for mydevice in deviceslst:
        children = await client.get_children_for_device(mydevice["deviceId"])
        if children == None:
            async_add_devices([IntegrationBlueprintBinarySwitch(client, mydevice["deviceId"], mydevice["deviceId"], mydevice["alias"])])
        else:
            for child in children:
                async_add_devices([IntegrationBlueprintBinarySwitch(client, mydevice["deviceId"], child["id"], child["alias"])])

class IntegrationBlueprintBinarySwitch(SwitchEntity, TpLink_CloudEntity):
    """TpLink_Cloud switch class."""

    def __init__(self, client, deviceId, child_id, alias):
        self.client = client
        self.device = deviceId
        self.child_id = child_id
        self.alias = alias
        self.dev_state = None
        self.dev_alias = None

        # Tell the API client to call dev_update() when it gets an update
        self.client.set_callback_for_dev(self.device, self.dev_update)

    def dev_update(self):
        self.dev_state = self.client.get_state_sts(self.child_id)
        self.dev_alias = self.client.get_alias(self.child_id)
        
        # Tell HA we have an update
        self.schedule_update_ha_state()

    async def async_turn_on(self, **kwargs):  # pylint: disable=unused-argument
        """Turn on the switch."""
        await self.client.set_state_for_device(self.child_id, 1)

    async def async_turn_off(self, **kwargs):  # pylint: disable=unused-argument
        """Turn off the switch."""
        await self.client.set_state_for_device(self.child_id, 0)

    # Generic Properties
    @property
    def available(self):
        """Reports available."""
        if self.dev_state == None:
            return False
        else:
            return True

    @property
    def unique_id(self):
        return f"{self.child_id.lower()}"

    @property
    def name(self):
        if self.dev_alias == None:
            return
        return self.dev_alias

    @property
    def friendly_name(self):
        if self.dev_alias == None:
            return
        return self.dev_alias

    @property
    def icon(self):
        """Return the icon of this switch."""
        return "mdi:beach"

    @property
    def is_on(self):
        if self.dev_state == None:
            return 0
        return self.dev_state
