from dataclasses import dataclass; import platform
@dataclass
class Config: system:str=platform.system().lower()
