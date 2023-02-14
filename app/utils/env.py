import os
from enum import Enum
from typing import Any, Callable, Optional, Type, TypeVar

import orjson as json

T = TypeVar("T")
ENUM = TypeVar("ENUM", bound=Enum)


class Env:
    @classmethod
    def general_loader(
        cls: Type["Env"],
        name: str,  # 用于指定环境变量的名称
        loader: Callable[[str], T],  # 用于指定加载器
        default: T,  # 用于指定默认值
        description: Optional[str] = None,  # 用于描述环境变量的作用
        contains_secret: bool = False,  # 用于指定是否包含敏感信息, 包含敏感信息的环境变量应该在日志中隐藏
    ) -> T:
        value_str: Optional[str] = os.getenv(name, None)
        value: T = loader(value_str) if value_str is not None else default
        # TODO: log
        return value

    @classmethod
    def int(
        cls: Type["Env"],
        name: str,
        default: int = 0,
        description: Optional[str] = None,
        contains_secret: bool = False,
    ) -> int:
        return cls.general_loader(
            name=name,
            loader=lambda v: int(v),
            default=default,
            description=description,
            contains_secret=contains_secret,
        )

    @classmethod
    def float(
        cls: Type["Env"],
        name: str,
        default: float = 0.0,
        description: Optional[str] = None,
        contains_secret: bool = False,
    ) -> float:
        return cls.general_loader(
            name=name,
            loader=lambda v: float(v),
            default=default,
            description=description,
            contains_secret=contains_secret,
        )

    @classmethod
    def json(
        cls: Type["Env"],
        name: str,
        default: Optional[Any] = None,
        description: Optional[str] = None,
        contains_secret: bool = False,
    ) -> Any:
        return cls.general_loader(
            name=name,
            loader=lambda v: json.loads(v),
            default=default,
            description=description,
            contains_secret=contains_secret,
        )

    @classmethod
    def string(
        cls: Type["Env"],
        name: str,
        default: str = "",
        description: Optional[str] = None,
        contains_secret: bool = False,
    ) -> str:
        return cls.general_loader(
            name=name,
            loader=lambda v: str(v),
            default=default,
            description=description,
            contains_secret=contains_secret,
        )

    @classmethod
    def enum(
        cls: Type["Env"],
        name: str,
        enum_class: Type[ENUM],
        default: ENUM,
        description: Optional[str] = None,
        contains_secret: bool = False,
    ) -> ENUM:
        return cls.general_loader(
            name=name,
            loader=lambda v: enum_class(enum_class.mro()[1](v)),
            default=default,
            description=description,
            contains_secret=contains_secret,
        )

    @classmethod
    def boolean(
        cls: Type["Env"],
        name: str,
        default: bool = False,
        description: Optional[str] = None,
        contains_secret: bool = False,
    ) -> bool:
        return cls.general_loader(
            name=name,
            loader=lambda v: bool(v),
            default=default,
            description=description,
            contains_secret=contains_secret,
        )

    @classmethod
    def auto_load(
        cls: Type["Env"],
        name: Optional[None] = None,
        settings: Any = None,
    ) -> None:
        if name is None or settings is None:
            import inspect

            stack = inspect.stack()
            try:
                f_locals = stack[1][0].f_locals
                if name is None:
                    name = f_locals["__name__"]
                if settings is None:
                    settings = f_locals
            finally:
                del stack

        if "." not in str(name):
            raise Exception(f"Invalid settings module name {name}. Please import it with full package name")
        sep = "__"
        settings_prefix = str(name).replace(".", sep)
        # print('load settings from env for %s' % settings_prefix)
        for key, value in os.environ.items():
            if not key.startswith(settings_prefix):
                continue
            key = key[len(settings_prefix) + len(sep) :]
            if not key or sep in key:
                continue
            if key in settings and settings[key] is not None and not isinstance(settings[key], str):
                try:
                    value = json.loads(value)
                except Exception:
                    import ast

                    value = ast.literal_eval(value)

            settings[key] = value