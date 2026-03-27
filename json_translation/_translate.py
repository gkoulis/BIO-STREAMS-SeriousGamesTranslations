"""
Author: Dimitris Gkoulis
Created on: Wednesday 23 July 2025
"""

__all__ = ["translate_json_file"]

import json
import time

from typing import Any, Literal, Union, Optional

from deep_translator import GoogleTranslator
from ._cache import instantiate_internals, insert, get_first_by_source


class _Context:
    def __init__(self) -> None:
        self.key_list: Union[Literal["*"], list[str]] = []
        self.source_language: str = ""
        self.target_language: str = ""
        self.caching1: bool = True
        self.caching2: bool = True
        self.cache: dict[str, str] = {}

    def should_translate_key(self, key: str) -> bool:
        if type(self.key_list) == str and self.key_list == "*":
            return True
        return key in self.key_list


_C: _Context = _Context()


def _translate_string(string: str, source_language: str, target_language: str) -> str:
    if isinstance(string, str):
        if string.strip() == "":
            return ""
        try:
            return GoogleTranslator(
                source=source_language, target=target_language
            ).translate(string)
        except Exception as ex:
            print(f"⚠️ Error translating '{string}': {ex}")
            return string
    raise TypeError(f"Invalid type: {type(string)}")


def _translate_json(data: Any, key: str, full_key: str) -> Any:
    if isinstance(data, dict):
        new_dict: dict = {}
        for key, value in data.items():
            full_key_: str = f"{full_key}.{key}"
            new_value = _translate_json(data=value, key=key, full_key=full_key_)
            new_dict[key] = new_value
        return new_dict

    elif isinstance(data, list):
        new_list: list = []
        for index, element in enumerate(data):
            full_key_: str = f"{full_key}.{index}"
            new_element = _translate_json(data=element, key=key, full_key=full_key_)
            new_list.append(new_element)
        return new_list

    elif isinstance(data, str):
        if _C.should_translate_key(key=key) is False:
            return data

        if _C.caching1 is True:
            if data in _C.cache:
                print(
                    f"Cache1 HIT:",
                    _C.source_language,
                    "->",
                    _C.target_language,
                    full_key,
                    key,
                    f"{data[0:97]}..." if len(data) > 100 else data,
                )
                return _C.cache[data]

        if _C.caching2 is True:
            result: Optional[tuple[str, str, str, str]] = get_first_by_source(
                source_language=_C.source_language,
                source_value=data,
                target_language=_C.target_language,
            )
            if result is not None:
                assert result[0] == _C.source_language
                assert result[1] == data
                assert result[2] == _C.target_language

                if _C.caching1 is True:
                    _C.cache[data] = result[3]

                print(
                    f"Cache2 HIT:",
                    _C.source_language,
                    "->",
                    _C.target_language,
                    full_key,
                    key,
                    f"{data[0:97]}..." if len(data) > 100 else data,
                )
                return result[3]

        print(
            f"Translating:",
            _C.source_language,
            "->",
            _C.target_language,
            full_key,
            key,
            f"{data[0:97]}..." if len(data) > 100 else data,
        )
        translated_data: str = _translate_string(
            string=data,
            source_language=_C.source_language,
            target_language=_C.target_language,
        )

        if _C.caching1 is True:
            _C.cache[data] = translated_data

        if _C.caching2 is True:
            insert(
                source_language=_C.source_language,
                source_value=data,
                target_language=_C.target_language,
                target_value=translated_data,
            )

        return translated_data

    else:
        return data


def translate_json_file(
    source_language: str,
    target_language: str,
    key_list: Union[Literal["*"], list[str]],
    input_file_path: str,
    output_file_path: str,
    caching1: bool = True,
    caching2: bool = True,
    indent: int = 2,
    database_name: str = "default.db",
) -> None:
    start_t: int = time.time_ns()

    assert source_language != target_language

    _C.source_language = source_language
    _C.target_language = target_language
    _C.key_list = key_list
    _C.caching1 = caching1
    _C.caching2 = caching2
    _C.cache = {}

    if caching2 is True:
        instantiate_internals(name=database_name)

    with open(input_file_path, "r", encoding="utf-8") as input_file:
        input_data: dict = json.load(input_file)

    output_data: dict = _translate_json(data=input_data, key="root", full_key="root")

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        json.dump(output_data, output_file, ensure_ascii=False, indent=indent)

    end_t: int = time.time_ns()
    diff_t: int = end_t - start_t
    print(f"Finished after {diff_t / 1_000_000_000} secs")


def main() -> None:
    translate_json_file(
        source_language="en",
        target_language="el",
        key_list=["title", "description", "question", "text"],
        input_file_path="./example/content-theme-list.en.json",
        output_file_path="./example/content-theme-list.el.json",
        indent=4,
    )


if __name__ == "__main__":
    main()
