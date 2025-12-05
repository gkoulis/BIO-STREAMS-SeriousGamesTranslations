"""
Author: Dimitris Gkoulis
Created on: Friday 05 December 2025
"""

import json
import pprint

import pandas as pd

_IGNORE_EN: bool = True
_DEBUG: bool = False
_SUFFIX: str = "-NEW-20251205.json"


def _set_by_path(json_dict: dict, path: str, value: str) -> None:
    if path.startswith("root."):
        path = path.replace("root.", "")
    
    parts = path.split(".")
    current = json_dict
    
    for i, part in enumerate(parts):
        # Convert numeric parts to integers (list indexes)
        if part.isdigit():
            part = int(part)
        
        # If this is the last segment — assign the value
        if i == len(parts) - 1:
            current[part] = value
            return
        
        current = current[part]


def _move_translations_from_spreadsheet_to_json(language_code: str, family: str) -> None:
    path_to_spreadsheet: str = f"/home/dgk/projects/json_trans/data/spreadsheets/{language_code}/{family}.xlsx"
    df: pd.DataFrame = pd.read_excel(path_to_spreadsheet, dtype={language_code: str})
    record_list: list[dict] = df.to_dict(orient="records")
    
    # --------------------------------------------------
    
    path_to_json: str = f"/home/dgk/projects/json_trans/data/json/{language_code}/{family}.json"
    with open(path_to_json, "r", encoding="utf-8") as input_json_file:
        json_dict: dict = json.load(input_json_file)
    
    # --------------------------------------------------
    
    for record in record_list:
        if _DEBUG is True:
            if "full_key" not in record:
                print(path_to_spreadsheet, path_to_json)
                pprint.pprint(record, sort_dicts=False)
                exit(1)
        else:
            assert "full_key" in record
        
        full_key: str = record["full_key"]
        should_translate = record["should_translate"] in [True, "true", "True", "1", 1, "yes", "Yes", "YES"]
        content = record[language_code]
        if type(content) in [int]:
            content = str(content)
        if _DEBUG is True:
            if type(content) != str:
                print(f"converting content {content} ({type(content)}) to string")
                print(path_to_spreadsheet, path_to_json)
                pprint.pprint(record, sort_dicts=False)
                content = str(content)
                exit(1)
        else:
            assert type(content) == str
        
        if should_translate is False:
            continue
        
        if _DEBUG is True:
            content = "TEST"
        _set_by_path(json_dict=json_dict, path=full_key, value=content)
    
    # --------------------------------------------------
    
    output_path_to_file: str = path_to_json
    output_path_to_file = output_path_to_file.replace(".json", _SUFFIX)
    with open(output_path_to_file, "w", encoding="utf-8") as f:
        json.dump(json_dict, f, ensure_ascii=False, indent=4)


def main() -> None:
    language_code_list: list[str] = ["bg", "da", "el", "en", "es", "fr", "nl", "pt", "sl", "sv"]
    family_list: list[str] = ["FoodNinja", "FoodQuiz", "JS"]
    
    for language_code in language_code_list:
        if _IGNORE_EN is True:
            if language_code == "en":
                continue
        for family in family_list:
            _move_translations_from_spreadsheet_to_json(
                language_code=language_code,
                family=family,
            )


if __name__ == "__main__":
    main()
