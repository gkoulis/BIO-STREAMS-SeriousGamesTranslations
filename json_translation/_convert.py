"""
Author: Dimitris Gkoulis
Created on: Wednesday 23 July 2025
"""

__all__ = ["convert_json_to_excel"]

import json
from typing import Any, Union, Literal

import pandas as pd


class _Context:
    def __init__(self) -> None:
        self.key_list: Union[Literal["*"], list[str]] = []
        self.df_data: list[dict] = []

    def should_translate_key(self, key: str) -> bool:
        if type(self.key_list) == str and self.key_list == "*":
            return True
        return key in self.key_list


_C: _Context = _Context()


def _visit(data: Any, key: str, full_key: str) -> None:
    if isinstance(data, dict):
        for key, value in data.items():
            full_key_: str = f"{full_key}.{key}"
            _visit(data=value, key=key, full_key=full_key_)

    elif isinstance(data, list):
        for index, element in enumerate(data):
            full_key_: str = f"{full_key}.{index}"
            _visit(data=element, key=key, full_key=full_key_)

    elif isinstance(
        data,
        (
            str,
            int,
            bool,
            float,
        ),
    ):
        should_translate: bool = False
        if isinstance(data, str):
            should_translate = _C.should_translate_key(key=key)

        _C.df_data.append(
            {
                "full_key": full_key,
                "key": key,
                "should_translate": should_translate,
                "value_type": str(type(data)),
                "value": data,
                "value_translated": data,
            }
        )

    else:
        raise NotImplementedError


def convert_json_to_excel(
    key_list: Union[Literal["*"], list[str]],
    input_file_path: str,
    output_file_path: str,
) -> None:
    _C.key_list = key_list
    _C.df_data = []

    with open(input_file_path, "r", encoding="utf-8") as input_file:
        input_data: dict = json.load(input_file)

    _visit(data=input_data, key="root", full_key="root")

    df: pd.DataFrame = pd.DataFrame(data=_C.df_data)
    df["should_translate"] = df["should_translate"].astype(bool).astype(str)
    df["value_type"] = df["value_type"].astype(str)
    df["value"] = df["value"].astype(str)
    df["value_translated"] = df["value_translated"].astype(str)
    df.to_excel(output_file_path)
