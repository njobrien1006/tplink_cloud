"""BlueprintEntity class"""
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, NAME, VERSION, ATTRIBUTION


class TpLink_CloudEntity(Entity):
    """Cloud Entity"""

    @property
    def unique_id(self):
        """Return a unique ID to use for this entity."""
        return self.device

    @property
    def device_info(self):
        """DevInfo"""
        mydevice = self.client.sync_rtn_device(self.device)
        return {
            "identifiers": {(DOMAIN, self.device)},
            "name": mydevice["alias"],
            "model": mydevice["deviceModel"],
            "sw_version": mydevice["fwVer"],
            "manufacturer": NAME,
        }

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        return {
            "attribution": ATTRIBUTION,
            "integration": DOMAIN,
        }
