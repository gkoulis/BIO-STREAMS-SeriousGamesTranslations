"""
Author: Dimitris Gkoulis
Created on: Wednesday 23 July 2025
"""

__all__ = ["join_convert_json_to_excel"]

import json
from dataclasses import dataclass
from typing import Any, Union, Literal

import pandas as pd


@dataclass
class _Entry:
    full_key: str
    key: str
    should_translate: bool
    value_type: str
    value: str


class _Context:
    def __init__(self) -> None:
        self.key_list: Union[Literal["*"], list[str]] = []
        self.source_by_full_key: dict[str, _Entry] = {}
        self.target_by_full_key: dict[str, _Entry] = {}

    def should_translate_key(self, key: str) -> bool:
        if type(self.key_list) == str and self.key_list == "*":
            return True
        return key in self.key_list


_C: _Context = _Context()


def _visit(data: Any, key: str, full_key: str, source: bool) -> None:
    if isinstance(data, dict):
        for key, value in data.items():
            full_key_: str = f"{full_key}.{key}"
            _visit(data=value, key=key, full_key=full_key_, source=source)

    elif isinstance(data, list):
        for index, element in enumerate(data):
            full_key_: str = f"{full_key}.{index}"
            _visit(data=element, key=key, full_key=full_key_, source=source)

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

        entry: _Entry = _Entry(
            full_key=full_key,
            key=key,
            should_translate=should_translate,
            value_type=str(type(data)),
            value=data,
        )

        if source is True:
            print(full_key)
            assert full_key not in _C.source_by_full_key
            _C.source_by_full_key[full_key] = entry
        else:
            assert full_key not in _C.target_by_full_key
            _C.target_by_full_key[full_key] = entry

    else:
        raise NotImplementedError


def join_convert_json_to_excel(
    source_language: str,
    target_language: str,
    key_list: Union[Literal["*"], list[str]],
    source_input_file_path: str,
    target_input_file_path: str,
    output_file_path: str,
) -> None:
    _C.key_list = key_list
    _C.source_by_full_key = {}
    _C.target_by_full_key = {}

    with open(source_input_file_path, "r", encoding="utf-8") as source_input_file:
        source_input_data: dict = json.load(source_input_file)

    with open(target_input_file_path, "r", encoding="utf-8") as target_input_file:
        target_input_data: dict = json.load(target_input_file)

    _visit(data=source_input_data, key="root", full_key="root", source=True)
    _visit(data=target_input_data, key="root", full_key="root", source=False)

    assert len(_C.source_by_full_key) == len(_C.target_by_full_key)

    df_data: list[dict] = []

    for key1, entry1 in _C.source_by_full_key.items():
        assert key1 in _C.target_by_full_key
        entry2 = _C.target_by_full_key[key1]
        assert entry1.full_key == entry2.full_key
        assert entry1.key == entry2.key
        assert entry1.should_translate == entry2.should_translate
        assert entry1.value_type == entry2.value_type
        row = {
            "full_key": entry1.full_key,
            "key": entry1.key,
            "should_translate": entry1.should_translate,
            "value_type": entry1.value_type,
            source_language: entry1.value,
            target_language: entry2.value,
        }
        df_data.append(row)

    df: pd.DataFrame = pd.DataFrame(data=df_data)
    df["should_translate"] = df["should_translate"].astype(bool).astype(str)
    df["value_type"] = df["value_type"].astype(str)
    df[source_language] = df[source_language].astype(str)
    df[target_language] = df[target_language].astype(str)
    df.to_excel(output_file_path)
