
import plistlib
import asyncio
from typing import List
from enum import Flag
import ipaddress

import requests
import zeroconf
import pyatv
from pyatv.conf import AppleTV
from pyatv.support.rtsp import RtspSession
from pyatv.protocols.airplay.remote_control import RemoteControl as AirPlayRemoteControl

from . import log
from .utils import SimpleRepr


class AirplayFeatures(Flag):
    # https://openairplay.github.io/airplay-spec/features.html
    Video = 2**0
    Photo = 2**1
    VideoFairPlay = 2**2
    VideoVolumeControl = 2**3
    VideoHTTPLiveStreams = 2**4
    Slideshow = 2**5
    # bit 6 blank
    Screen = 2**7
    ScreenRotate = 2**8
    Audio = 2**9
    # bit 10 blank
    AudioRedundant = 2**11
    FPSAPv2pt5_AES_GCM = 2**12
    PhotoCaching = 2**13
    Authentication4 = 2**14
    MetadataFeature1 = 2**15
    MetadataFeature2 = 2**16
    MetadataFeature0 = 2**17
    AudioFormat1 = 2**18
    AudioFormat2 = 2**19
    AudioFormat3 = 2**20
    AudioFormat4 = 2**21
    # bit 22 blank
    Authentication1 = 2**23
    # 24-25 blank
    HasUnifiedAdvertiserInfo = 2**26
    SupportsLegacyPairing = 2**27
    # 28-29 blank
    RAOP = 2**30
    # 31
    IsCarPlay = 2**32
    SupportsVolume = 2**32 # the same
    SupportsAirPlayVideoPlayQueue = 2**33
    SupportsAirPlayFromCloud = 2**34
    # 35-37
    SupportsCoreUtilsPairingAndEncryption = 2**38
    # 39
    SupportsBufferedAudio = 2**40 # multi-room audio
    SupportsPTP = 2**41 # multi-room audio
    SupportsScreenMultiCodec = 2**42
    SupportsSystemPairing = 2**43
    # 44-45
    SupportsHKPairingAndAccessControl = 2**46
    SupportsTransientPairing = 2**48
    MetadataFeature4 = 2**50
    SupportsUnifiedPairSetupAndMFi = 2**51
    SupportsSetPeersExtendedMessage = 2**52

    @classmethod
    def from_bits(cls, bits):
        flags = cls(0)
        for flag in cls:
            if flag.value & bits:
                flags |= flag
        return flags

class AirplayReceiverStatus(Flag):
    ProblemDetected = 2**0
    DeviceNotConfigured = 2**1
    AudioCableAttached = 2**2
    PINRequired = 2**3
    SupportsAirPlayFromCloud = 2**6
    PasswordRequried = 2**7
    OneTimePairingRequired = 2**9
    DeviceWasSetupForHKAccessControl = 2**10
    DeviceSupportsRelay = 2**11
    SilentPrimary = 2**12
    TightSyncIsGroupLeader = 2**13
    TightSyncBuddyNotReachable = 2**14
    IsAppleMusicSubscriber = 2**15
    CloudLibraryIsOn = 2**16 # iCML
    ReceiverSessionIsActive = 2**17

    @classmethod
    def from_bits(cls, bits):
        flags = cls(0)
        for flag in cls:
            if flag.value & bits:
                flags |= flag
        return flags

class AirplayReceiver(SimpleRepr):
    def __init__(
            self, name: str, service_info: zeroconf.ServiceInfo,
            loop: asyncio.events.AbstractEventLoop = None,
        ):
        if not loop:
            try:
                loop = asyncio.get_running_loop()
            except RuntimeError as e:
                loop = asyncio.new_event_loop()
        self.loop = loop
        self.name = name
        self.service_info = service_info
        self.service_properties = {
            k.decode(): v.decode() for k, v in service_info.properties.items()
        }

        self._pyatv_device_service = None
        self._pyatv_device_config = None
        self._pyatv_rtsp_session = None

        # for name, value in kwargs.items():
        #     setattr(self, name, value)

    def _scan_for_device_sync(self):
        fut_res = self._scan_for_device()
        return asyncio.run(fut_res)

    # async def _scan_for_device(self) -> AppleTV:
    #     """This method *should* find the pyatv device for this Receiver"""
    #     addresses = self._get_ipv4_addresses()
    #     log.debug(f"starting scan for device at address {addresses}")
    #
    #     # TODO choose address based on interface metric
    #
    #     self._pyatv_device_config = AppleTV(ipaddress.ip_address(addresses[0]), self.name)
    #
    #     service = await self._get_pyatv_airplay_service()
    #     self._pyatv_device_config.add_service(service)
    #
    #     return self._pyatv_device_config
    #
    # async def _get_pyatv_airplay_service(self, force_new=False):
    #     if not self._pyatv_device_service or force_new:
    #         self._pyatv_device_service = pyatv.conf.ManualService(
    #             self.name,
    #             protocol=pyatv.const.Protocol.AirPlay,
    #             port=self.service_info.port,
    #             properties=self.service_properties,
    #         )
    #     return self._pyatv_device_service

    async def _get_pyatv_rtsp_session(self):
        # TODO check state of connection
        if not self._pyatv_rtsp_session:
            # http_conn = pyatv.support.http.HttpConnection()
            transport, protocol = await self.loop.create_connection(
                lambda: pyatv.support.http.HttpConnection(),
                self._get_ip_addresses()[0],
                self.service_info.port - 1, # HACK?
            )
            self._pyatv_rtsp_session = RtspSession(
                protocol,
            )
        return self._pyatv_rtsp_session

    def parse_service_properties(self, **kwargs):
        # TODO set defaults for following expected properties and convert types
        # kwargs properties:
        self.model = kwargs.get("model", None) #: str = # None
        self.manufacturer = kwargs.get("manufacturer", None) #: str = # None
        self.serialNumber = kwargs.get("serialNumber", None) #: str = # None
        self.fv = kwargs.get("fv", None) #: str = # None
        self.osvers = kwargs.get("osvers", None) #: str = # None
        self.deviceid = kwargs.get("deviceid", None) #: str = # None
        self.pw = kwargs.get("pw", None) #: bool = # None
        self.acl = kwargs.get("acl", None) #: int = # None
        self.srcvers = kwargs.get("srcvers", None) # = # None
        self.gcgl = kwargs.get("gcgl", None) #: bool = # None
        self.igl = kwargs.get("igl", None) #: bool = # None
        self.gpn = kwargs.get("gpn", None) #: str = # None
        self.hmid = kwargs.get("hmid", None) #: str = # None
        self.pgcgl = kwargs.get("pgcgl", None) #: bool = # None
        self.protovers = kwargs.get("protovers", None) #: str = # None
        # # hex
        # pk = # None
        # rsf = # None
        # # UUID
        # pi = # None
        # psi = # None
        # gid = # None
        # hgid = # None
        # pgid = # None
        # tsid = # None

    @property
    def features(self) -> AirplayFeatures:
        features = self.service_properties.get("features", 0) #: AirplayFeatures = # None
        features = int(features, 0)
        features = AirplayFeatures.from_bits(features)
        return features

    @property
    def status(self) -> AirplayReceiverStatus:
        flags = self.service_properties.get("flags", 0) #: AirplayReceiverStatus
        flags = int(flags, 0)
        self.flags = AirplayReceiverStatus.from_bits(flags)

    def update_service_info(self, new_info):
        self.service_info = new_info
        self.service_properties = {
            k.decode(): v.decode() for k, v in self.service_info.properties.items()
        }

        # # look for device given new ip addresses
        # # TODO eventually should relegate this to only once the user shows interest in the device
        # if not self._pyatv_device_config:
        #     future = asyncio.ensure_future(self._scan_for_device())
        #
        # if not self._pyatv_device_service:
        #     future = asyncio.ensure_future(self._get_pyatv_airplay_service(force_new=True))

        # future = asyncio.ensure_future(self._get_server_info())

    @property
    def friendly_name(self) -> str:
        return self.name.replace("._airplay._tcp.local.", "")

    @property
    def list_entry_name(self) -> str:
        return f"{self.friendly_name} (at {self.service_info.server})"

    def _get_ip_addresses(self) -> List:
        return self.service_info.parsed_addresses()

    def _get_ipv4_addresses(self) -> List:
        return self.service_info.parsed_addresses(zeroconf.IPVersion.V4Only)

    @property
    def ip_address(self):
        return self._get_ip_addresses()[0]

    async def _get_server_info(self):
        rtsp_session = await self._get_pyatv_rtsp_session()
        log.debug(f"acquiring server info ...")
        info = await rtsp_session.info()
        log.debug(f"got info: {info}")
        self._server_rtsp_info = info
        return info

if __name__ == "__main__":
    test_features = {
        "RPiPlay": "0x5A7FFEE6",
        # "UxPlay": "0x5A7FFEE6",
    }

    for name, example in test_features.items():
        ex_int = int(example, 0)
        features = AirplayFeatures.from_bits(ex_int)
        print(f"{name} bits: {example}")
        print(f"{name} features: {features}")

    test_flags = {
        "RPiPlay Idle": "0x4",
    }

    for name, example in test_flags.items():
        ex_int = int(example, 0)
        flags = AirplayReceiverStatus.from_bits(ex_int)
        print(f"{name} bits: {example}")
        print(f"{name} flags: {flags}")
