"""Sample API Client."""
import logging
import asyncio
import socket
from typing import Optional
import aiohttp
import async_timeout
import uuid
import time

TIMEOUT = 30


_LOGGER: logging.Logger = logging.getLogger(__package__)

HEADERS = {"Content-type": "application/json"}


class IntegrationBlueprintApiClient:
    def __init__(
        self, username: str, password: str, session: aiohttp.ClientSession, hass
    ) -> None:
        """Sample API Client."""
        self._username = username
        self._password = password
        self._session = session
        self.hass = hass
        self.loop = hass.loop
        self._devices = None
        self._dev_sts = {}
        self._dev_alias = {}
        self._dev_rsp = {}
        self.dev_callbacks = {}
        self.url = "https://use1-wap.tplinkcloud.com"
        self.token = None
        self.url_token = None
        self.firsttime = True
        self.timeout = TIMEOUT

    async def async_url_token_update(self):
        """Get Token with User, Pass, UUID4"""
        _LOGGER.debug(f"Token Update Call.")
        _LOGGER.info(f"Token UUID: {uuid.uuid4().hex}")
        response = await self.api_wrapper("post", self.url, 
            data={
                "method": "login",
                "params": {
                    "appType": "Kasa_Android",
                    "cloudPassword": self._password,
                    "cloudUserName": self._username,
                    "terminalUUID": uuid.uuid4().hex
                }
                }, 
            headers=HEADERS)
        _LOGGER.debug(f"Token Update Call Rsp: {response}")
        if response != None:
            self.token = response["result"]["token"]
            self.url_token = f"{self.url}/?token={self.token}"
            _LOGGER.info(f"URL'd Token: {self.url_token}")
        else:
            _LOGGER.info(f"Token Failed Update!!")

    async def async_get_devices(self):
        """Get Devices from the Cloud."""
        if self.token == None:
            await self.async_url_token_update()
        response = await self.api_wrapper("post", self.url_token, data={"method": "getDeviceList"}, headers=HEADERS)
        if response == None:
            _LOGGER.debug(f"Async Get Devices failed with None.")
            return None
        _LOGGER.debug(f"Async Get Devices: {response}")
        """Set HTTP timeout to something normal."""
        self.timeout = 5 
        if response["error_code"] == -20651:
            await self.async_url_token_update()
            response = await self.api_wrapper("post", self.url_token, data={"method": "getDeviceList"}, headers=HEADERS)
            _LOGGER.debug(f"Async Get Devices Updated Tok: {response}")
            self._devices = response["result"]["deviceList"]
        else:
            self._devices = response["result"]["deviceList"]
        return self._devices

    async def async_rtn_devices(self):
        """Return Devices for Switch Config"""
        return self._devices

    def sync_rtn_device(self, devid):
        """Return Single Device to parse info for model in .entity"""
        for mydevice in self._devices:
            if devid == mydevice["deviceId"]:
                return mydevice
        return None

    def get_state_sts(self, devid):
        """Return Single State for a switch. Primary Scwitches are len(40), Children are len(42)"""
        if len(devid) > 40:
            dev = devid[0:40]
            if self._dev_sts[dev] == None:
                return None
            child = int(devid[-2:])
            return self._dev_sts[dev][child]
        else:
            if self._dev_sts[devid] == None:
                return None
            return self._dev_sts[devid]

    async def get_state_for_device(self, devid):
        """Parse the API response and return that."""
        if devid in self._dev_rsp:
            result = await self.get_parse_for_device(self._dev_rsp[devid], "result")
            rsp = await self.get_parse_for_device(result, "responseData")
            system = await self.get_parse_for_device(rsp, "system") 
            sysinfo = await self.get_parse_for_device(system, "get_sysinfo")
            if "children" in sysinfo:
                children = await self.get_parse_for_device(sysinfo, "children")
                stateinfo = []
                for child in children:
                    childstate = child["state"]
                    stateinfo.append(childstate)
            else:
                stateinfo =  sysinfo["relay_state"]
            return stateinfo
        return None

    def get_alias(self, devid):
        """Return Single Alias for a switch. Primary Scwitches are len(40), Children are len(42)"""
        if len(devid) > 40:
            dev = devid[0:40]
            child = int(devid[-2:])
            return self._dev_alias[dev][child]
        else:
            return self._dev_alias[devid]

    async def get_alias_for_device(self, devid):
        """Parse the API response and return that."""
        if devid in self._dev_rsp:
            result = await self.get_parse_for_device(self._dev_rsp[devid], "result")
            rsp = await self.get_parse_for_device(result, "responseData")
            system = await self.get_parse_for_device(rsp, "system") 
            sysinfo = await self.get_parse_for_device(system, "get_sysinfo")
            if "children" in sysinfo:
                children = await self.get_parse_for_device(sysinfo, "children")
                stateinfo = []
                for child in children:
                    childalias = child["alias"]
                    stateinfo.append(childalias)
            else:
                stateinfo =  sysinfo["alias"]
            return stateinfo

    async def set_state_for_device(self, child_id, state):
        'Use Async Loop incase multipe set request @ once.'
        self.hass.async_create_task(self.set_state_for_device_loop(child_id, state))

    async def set_state_for_device_loop(self, child_id, state):
        """Set state of switch and update our sts for assumed state if no error is returned."""
        if len(child_id) > 40:
            """Is Child"""
            deviceid = child_id[0:40]
            if self._dev_sts[deviceid] != None:
                response = await self.api_wrapper("post", self.url_token, 
                data={
                    "method": "passthrough",
                    "params": {
                        "deviceId":  deviceid.upper(),
                        "requestData": {
                            "context": {
                                "child_ids": [
                                    child_id.upper()
                                ],
                                "source": ""
                            },
                            "system": {
                                "set_relay_state": {
                                    "state": state
                                }
                            }
                        }
                    }
                    }, 
                headers=HEADERS)
                if response == None:
                    self._dev_sts[deviceid] = None
                else:
                    if response["error_code"] == 0:
                        child = int(child_id[-2:])
                        self._dev_sts[deviceid][child] = state
                    else:
                        _LOGGER.debug(f"Async Set Device Something Happened Child")
            else:
                await self.async_get_devices()
        else:
            """Is Not Child"""
            deviceid = child_id
            if self._dev_sts[deviceid] != None:
                response = await self.api_wrapper("post", self.url_token,
                data={
                    "method": "passthrough",
                    "params": {
                        "deviceId":  deviceid.upper(),
                        "requestData": {
                            "system": {
                                "set_relay_state": {
                                    "state": state
                                }
                            }
                        }
                    }
                    }, 
                headers=HEADERS)
                if response == None:
                    self._dev_sts[deviceid] = None
                else:
                    if response["error_code"] == 0:
                        self._dev_sts[deviceid] = state
                    else:
                        _LOGGER.debug(f"Async Set Device Something Happened N.Child")
            else:
                await self.async_get_devices()
        _LOGGER.debug(f"Async Set Device RSP for {self.get_alias(child_id)}: {response}")
        """Call to update our newly changed state within HA"""
        if deviceid in self.dev_callbacks:
                for callback in self.dev_callbacks[deviceid]:
                    callback()

    async def get_children_for_device(self, devid):
        """Parse the API response and return the children used to create the switches."""
        if devid in self._dev_rsp:
            result = await self.get_parse_for_device(self._dev_rsp[devid], "result")
            _LOGGER.debug(f"Async get_children_for_device: {result}")
            rsp = await self.get_parse_for_device(result, "responseData")
            system = await self.get_parse_for_device(rsp, "system") 
            sysinfo = await self.get_parse_for_device(system, "get_sysinfo")
            if "children" in sysinfo:
                children = await self.get_parse_for_device(sysinfo, "children")
                return children
            else:
                return None
        _LOGGER.debug(f"Async get_children_for_device not in RSP....offline")
        return "offline"

    async def get_parse_for_device(self, input, textparse):
        """Could't figure out how to parse the thing. Gave up and did what I could figure out without losing more hair."""
        return input[textparse]

    def set_callback_for_dev(self, dev_id, callback):
        """Register callbacks from the entities to be called later to update them."""
        if dev_id not in self.dev_callbacks:
            self.dev_callbacks[dev_id] = []
        self.dev_callbacks[dev_id].append(callback)

    async def async_get_data(self):
        """Get Specific Device Data for each device from the API."""
        _LOGGER.debug(f"Async Get Data Strt: {time.time()}")
        if self.token == None:
            await self.async_url_token_update()
        if self._devices == None:
            await self.async_get_devices()
        for device in self._devices:
            deviceid = device["deviceId"]
            if self.firsttime:
                await self.async_get_dev_data(deviceid)   
            else:
                self.hass.async_create_task(self.async_get_dev_data(deviceid))
        self.firsttime = False
        _LOGGER.debug(f"Async Get Data End: {time.time()}")

    async def async_get_dev_data(self, deviceid):
        """Get Specific Device Data for each device from the API."""
        if None == None:
            response = await self.api_wrapper("post", self.url_token, 
                data={
                    "method": "passthrough",
                    "params": {
                        "deviceId": deviceid,
                        "requestData": {
                            "system": {
                                "get_sysinfo": {}
                            }
                        }
                    }
                    }, 
                headers=HEADERS)
            _LOGGER.debug(f"Async Get Device RSP: {response}")
            if response["error_code"] == -20571:
                self._dev_sts[deviceid] = None
            elif response["error_code"] == -20651:
                """Token expires on monthly basis need to catch it an regenerate it."""
                await self.async_url_token_update()
                _LOGGER.warning(f"Token Updated due to Expired Creds. ReRun this Sub and Return @ Completion. Hopefully no Cont Loops.")
                await self.async_get_data()
                return
            elif response != None:
                self._dev_rsp[deviceid] = response
                self._dev_sts[deviceid] = await self.get_state_for_device(deviceid)
                self._dev_alias[deviceid] = await self.get_alias_for_device(deviceid)
                _LOGGER.debug(f"Async Get Device Relay Sts: {self._dev_sts[deviceid]}") 
            else:
                _LOGGER.warning(f"Async Get Device Failed with None Type Reponse: {response}")
            if deviceid in self.dev_callbacks:
                for callback in self.dev_callbacks[deviceid]:
                    if deviceid in self._dev_alias:
                        callback()
                    else:
                        self._dev_alias[deviceid] = "Offline"
                        callback()
        _LOGGER.debug(f"Async Get Data Dev End: {time.time()}")

    async def start(self):
        """Called after the integration is configured. Gets data and registers a future call."""
        await self.async_get_data()
        delay = 10
        self.task = self.loop.call_later(delay, self.syncmain)

    def syncmain(self):
        """To register future, it needed to be a def. Then we tack the Main back onto Async."""
        self.hass.async_create_task(self.main())

    async def main(self):
        """Run Get Data again and loop to Kill is called."""
        delay = 300
        _LOGGER.info(f"Call_Later in: {delay} seconds")
        self.task = self.loop.call_later(delay, self.syncmain)
        await self.async_get_data()

    async def kill(self):
        if self.task != None:
            _LOGGER.info(f"Killing Task")
            self.task.cancel()
            self.task = None
            _LOGGER.debug(f"Task Info: {self.task}")
        else:
            _LOGGER.info(f"Task Already Dead")

    async def api_wrapper(
        self, method: str, url: str, data: dict = {}, headers: dict = {}
    ) -> dict:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(self.timeout, loop=asyncio.get_event_loop()):
                if method == "get":
                    response = await self._session.get(url, headers=headers)
                    return await response.json()

                elif method == "put":
                    await self._session.put(url, headers=headers, json=data)

                elif method == "patch":
                    await self._session.patch(url, headers=headers, json=data)

                elif method == "post":
                    response = await self._session.post(url, headers=headers, json=data)
                    return await response.json()

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)
