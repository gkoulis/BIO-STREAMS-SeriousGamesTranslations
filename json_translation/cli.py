"""
Author: Dimitris Gkoulis
Created on: Wednesday 23 July 2025
"""

from typing import Union

import fire


# noinspection PyMethodMayBeStatic
class CLI:
    def convert_json_to_excel(
        self,
        key_list: Union[str, tuple],
        input_file_path: str,
        output_file_path: str,
    ) -> None:
        from ._convert import convert_json_to_excel

        if type(key_list) == str:
            assert key_list == "*"
        elif type(key_list) == tuple:
            key_list = list(key_list)
        else:
            raise ValueError(
                f"key_list '{key_list}' has invalid type: {type(key_list)}"
            )

        convert_json_to_excel(
            key_list=key_list,
            input_file_path=input_file_path,
            output_file_path=output_file_path,
        )

    def join_convert_json_to_excel(
        self,
        source_language: str,
        target_language: str,
        key_list: Union[str, tuple],
        source_input_file_path: str,
        target_input_file_path: str,
        output_file_path: str,
    ) -> None:
        from ._join_convert import join_convert_json_to_excel

        if type(key_list) == str:
            assert key_list == "*"
        elif type(key_list) == tuple:
            key_list = list(key_list)
        else:
            raise ValueError(
                f"key_list '{key_list}' has invalid type: {type(key_list)}"
            )

        join_convert_json_to_excel(
            source_language=source_language,
            target_language=target_language,
            key_list=key_list,
            source_input_file_path=source_input_file_path,
            target_input_file_path=target_input_file_path,
            output_file_path=output_file_path,
        )

    def translate(
        self,
        source_language: str,
        target_language: str,
        key_list: Union[str, tuple],
        input_file_path: str,
        output_file_path: str,
        indent: int = 4,
    ) -> None:
        from ._translate import translate_json_file

        if type(key_list) == str:
            assert key_list == "*"
        elif type(key_list) == tuple:
            key_list = list(key_list)
        else:
            raise ValueError(
                f"key_list '{key_list}' has invalid type: {type(key_list)}"
            )

        translate_json_file(
            source_language=source_language,
            target_language=target_language,
            key_list=key_list,
            input_file_path=input_file_path,
            output_file_path=output_file_path,
            indent=indent,
        )


def main() -> None:
    fire.Fire(CLI)


if __name__ == "__main__":
    main()
