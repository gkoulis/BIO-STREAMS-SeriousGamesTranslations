from ._translate import translate_json_file
from ._join_convert import join_convert_json_to_excel


def _translate__wrapper(
    food_ninja_1: bool, food_ninja_2: bool, food_quiz_1: bool
) -> None:
    source_language: str = "en"
    target_language_list: list[str] = [
        "bg",
        "da",
        "el",
        "es",
        "fr",
        "nl",
        "pt",
        "sl",
        "sv",
        # "bg", "da", "el",
        # "es", "fr", "nl",
        # "pt", "sl", "sv"
    ]
    indent: int = 2

    # --------------------------------------------------

    assert len(target_language_list) > 0
    assert indent in [2, 4]

    # Food Ninja (1/2)
    # --------------------------------------------------

    if food_ninja_1 is True:

        key_list: list[str] = ["title", "description", "messages"]
        for target_language in target_language_list:
            input_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/public/sr-foodninjastorymode/{source_language}/content-theme-list.json"
            )
            output_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/public/sr-foodninjastorymode/{target_language}/content-theme-list.json"
            )
            translate_json_file(
                source_language=source_language,
                target_language=target_language,
                key_list=key_list,
                input_file_path=input_file_path,
                output_file_path=output_file_path,
                indent=indent,
            )

    # Food Ninja (2/2)
    # --------------------------------------------------

    if food_ninja_2 is True:

        key_list: list[str] = ["name", "categoryName"]
        for target_language in target_language_list:
            input_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/public/sr-foodninjastorymode/{source_language}/content-item-list.json"
            )
            output_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/public/sr-foodninjastorymode/{target_language}/content-item-list.json"
            )
            translate_json_file(
                source_language=source_language,
                target_language=target_language,
                key_list=key_list,
                input_file_path=input_file_path,
                output_file_path=output_file_path,
                indent=indent,
            )

    # Food Quiz (1/1)
    # --------------------------------------------------

    if food_quiz_1 is True:

        key_list: list[str] = ["title", "description", "question", "text", "messages"]
        for target_language in target_language_list:
            input_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/public/sr-foodquizstorymode/{source_language}/content-theme-list.json"
            )
            output_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/public/sr-foodquizstorymode/{target_language}/content-theme-list.json"
            )
            translate_json_file(
                source_language=source_language,
                target_language=target_language,
                key_list=key_list,
                input_file_path=input_file_path,
                output_file_path=output_file_path,
                indent=indent,
            )


def _join_convert_json_to_excel__wrapper(
    food_ninja_1: bool, food_ninja_2: bool, food_quiz_1: bool, js_code_1: bool
) -> None:
    source_language: str = "en"
    target_language_list: list[str] = [
        "bg",
        "da",
        "el",
        "es",
        "fr",
        "nl",
        "pt",
        "sl",
        "sv",
    ]

    # Food Ninja (1/2)
    # --------------------------------------------------

    if food_ninja_1 is True:

        key_list: list[str] = ["title", "description", "messages"]
        for target_language in target_language_list:
            source_input_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/public/sr-foodninjastorymode/{source_language}/content-theme-list.json"
            )
            target_input_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/public/sr-foodninjastorymode/{target_language}/content-theme-list.json"
            )
            output_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/Translations/{source_language}-{target_language}-FoodNinja-ContentThemeList.xlsx"
            )
            join_convert_json_to_excel(
                source_language=source_language,
                target_language=target_language,
                key_list=key_list,
                source_input_file_path=source_input_file_path,
                target_input_file_path=target_input_file_path,
                output_file_path=output_file_path,
            )

    # Food Ninja (2/2)
    # --------------------------------------------------

    if food_ninja_2 is True:

        key_list: list[str] = ["name", "categoryName"]
        for target_language in target_language_list:
            source_input_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/public/sr-foodninjastorymode/{source_language}/content-item-list.json"
            )
            target_input_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/public/sr-foodninjastorymode/{target_language}/content-item-list.json"
            )
            output_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/Translations/{source_language}-{target_language}-FoodNinja-ContentItemList.xlsx"
            )
            join_convert_json_to_excel(
                source_language=source_language,
                target_language=target_language,
                key_list=key_list,
                source_input_file_path=source_input_file_path,
                target_input_file_path=target_input_file_path,
                output_file_path=output_file_path,
            )

    # Food Quiz
    # --------------------------------------------------

    if food_quiz_1 is True:

        key_list: list[str] = ["title", "description", "question", "text", "messages"]
        for target_language in target_language_list:
            source_input_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/public/sr-foodquizstorymode/{source_language}/content-theme-list.json"
            )
            target_input_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/public/sr-foodquizstorymode/{target_language}/content-theme-list.json"
            )
            output_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/Translations/{source_language}-{target_language}-FoodQuiz-ContentThemeList.xlsx"
            )
            join_convert_json_to_excel(
                source_language=source_language,
                target_language=target_language,
                key_list=key_list,
                source_input_file_path=source_input_file_path,
                target_input_file_path=target_input_file_path,
                output_file_path=output_file_path,
            )

    # JS Code
    # --------------------------------------------------

    if js_code_1 is True:

        key_list = "*"
        for target_language in target_language_list:
            source_input_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/src/locales/{source_language}.json"
            )
            target_input_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/src/locales/{target_language}.json"
            )
            output_file_path: str = (
                f"/home/dgk/projects/BIO-STREAMS/bio-streams-marketplace/Translations/{source_language}-{target_language}-JSCode.xlsx"
            )
            join_convert_json_to_excel(
                source_language=source_language,
                target_language=target_language,
                key_list=key_list,
                source_input_file_path=source_input_file_path,
                target_input_file_path=target_input_file_path,
                output_file_path=output_file_path,
            )


def main() -> None:
    # _translate__wrapper(food_ninja_1=True, food_ninja_2=False, food_quiz_1=True)
    _join_convert_json_to_excel__wrapper(
        food_ninja_1=True,
        food_ninja_2=False,
        food_quiz_1=True,
        js_code_1=True
    )


if __name__ == "__main__":
    main()
