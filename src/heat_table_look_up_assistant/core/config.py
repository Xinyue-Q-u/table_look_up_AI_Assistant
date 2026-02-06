from __future__ import annotations
import json
from dataclasses import dataclass, asdict, fields
from pathlib import Path
from typing import Any, get_type_hints

@dataclass
class AppConfig:
    model: str = "gpt-4.1"
    temperature: float = 0.0
    # max_tokens: int = 1024
    data_dir: Path = Path("./data")
    def __str__(self)-> str:
        """Human-readable pretty print."""
        lines=[
            "App Configuration:",
            f"model: {self.model}",
            f"temperature: {self.temperature}",
            f"data_dir: {self.data_dir}",
        ]
        return "\n".join(lines)

def _config_path(cfg: AppConfig) -> Path:
    return cfg.data_dir /"config.json"
def get_config_path() -> Path:
    cfg=load_config()
    return _config_path(cfg)


#transform config information to json format
def config_to_json(cfg: AppConfig) -> str:
    def default(o: Any):
        if isinstance(o, Path):
            return str(o)
        raise TypeError(f"Object of type {type(o)} is not JSON serializable")
    return json.dumps(asdict(cfg), indent=2, default=default)


def _coerce_value(raw: Any, target_type: Any) -> Any:
    if target_type is str:
        return raw

    if target_type is float:
        return float(raw)

    if target_type is int:
        return int(raw)

    if target_type is bool:
        s = raw.strip().lower()
        if s in {"true", "1", "yes", "y", "on"}:
            return True
        if s in {"false", "0", "no", "n", "off"}:
            return False
        raise ValueError("bool value must be one of: true/false, 1/0, yes/no, on/off")

    if target_type is Path:
        return Path(raw)
    raise TypeError(f"Unsupported config type: {target_type!r}")

def save_config(cfg: AppConfig) -> None:
    cfg.data_dir.mkdir(parents=True, exist_ok=True)
    path=_config_path(cfg)
    path.write_text(config_to_json(cfg),encoding="utf-8")
#load current config information
def load_config() -> AppConfig:
    """load App Configuration."""
    cfg=AppConfig()
    path=_config_path(cfg)
    if not path.exists():
        return cfg
    # if model_overrride is not None:
    #     cfg.model=model_overrride
    with path.open() as f:
        data=json.load(f)
    hints=get_type_hints(AppConfig)
    valid_keys=[f.name for f in fields(AppConfig)]
    for k,v in data.items():
        if k not in valid_keys:
            continue
        key=hints.get(k,type(getattr(cfg,k,None)))
        if key is Path:
            setattr(cfg,k,Path(v))
        else:
            setattr(cfg,k,v)
    return cfg

def set_config_value(key:str,value:Any) -> AppConfig:
    cfg=AppConfig()
    valid_keys=[f.name for f in fields(AppConfig)]
    if key not in valid_keys:
        raise ValueError(f"Invalid key {key}, valid keys are {valid_keys}")
    type_hints = get_type_hints(AppConfig)
    target_type = type_hints.get(key,type(getattr(cfg,key,None)))
    new_value=_coerce_value(value,target_type)
    setattr(cfg,key,new_value)
    save_config(cfg)
    return cfg
def get_config_value(key:str) -> Any:
    cfg=load_config()
    valid_keys={f.name for f in fields(AppConfig)}
    if key not in valid_keys:
        raise ValueError(f"Invalid key {key}, valid keys are {valid_keys}")
    return getattr(cfg,key)