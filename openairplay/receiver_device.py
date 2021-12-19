
from enum import Flag
import plistlib

import requests
import zeroconf

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
        ):
        self.name = name
        self.service_info = service_info
        self.service_properties = {
            k.decode(): v.decode() for k, v in service_info.properties.items()
        }

        # for name, value in kwargs.items():
        #     setattr(self, name, value)

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

    @property
    def friendly_name(self):
        return self.name.replace("._airplay._tcp.local.", "")

    @property
    def list_entry_name(self):
        return f"{self.friendly_name} (at {self.service_info.server})"

    def _get_ip_addresses(self):
        return self.service_info.parsed_addresses()

    @property
    def ip_address(self):
        return self._get_ip_addresses()[0]

    def _get_server_info(self):
        raise NotImplementedError()

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
