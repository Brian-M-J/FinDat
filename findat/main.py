import os
import fastcoref
import spacy
from fastcoref import spacy_component


def coref_resolution(file_path: str) -> str:
    """
    This function accepts a file path as input, opens the file, and
    performs coreference resolution on it using the fastcoref module.
    """
    nlp: spacy.lang.en.English = spacy.load("en_core_web_sm")
    nlp.add_pipe("fastcoref")
    text: str
    with open(file_path) as f:
        text = f.read()
    doc: spacy.tokens.doc.Doc = nlp(
        text, component_cfg={"fastcoref": {"resolve_text": True}}
    )
    return doc._.resolved_text


def process_directory(directory_path: str, key_string: str) -> dict[str, int]:
    """
    This function processes all the text files in a given directory.
    """
    file_occurrences: dict[str, int] = {}
    resolved_text: str
    file_name: str
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".txt"):
            if file_name in os.listdir(
                os.path.join(os.path.curdir, "resolved_text_files")
            ):
                with open(
                    os.path.join(os.path.curdir, "resolved_text_files", file_name),
                    mode="r",
                ) as file:
                    resolved_text = file.read()
            else:
                file_path: str = os.path.join(directory_path, file_name)
                resolved_text = coref_resolution(file_path)
                with open(
                    os.path.join(os.path.curdir, "resolved_text_files", file_name),
                    mode="x",
                ) as file:
                    file.write(resolved_text)

            occurrences: int = resolved_text.lower().count(key_string.lower())
            file_occurrences[file_name] = occurrences
    return file_occurrences


def sort_files_by_occurrences(
    directory_path: str, key_string: str
) -> list[tuple[str, int]]:
    """
    Function to generate a list of file names in descending order
    based on the number of occurrences of the key string.
    """
    file_occurrences: dict[str, int] = process_directory(directory_path, key_string)
    return sorted(file_occurrences.items(), key=lambda x: x[1], reverse=True)


# Example usage
def main() -> None:
    """
    Process all text files in a directory specified by the user.
    Output a list of file names in descending order of the number of times
    they occur in the files.
    """
    directory_path: str = input(
        "Please enter the directory where the text files to be scanned are kept: "
    )
    key_string: str = input("\nPlease enter the key string to search in the files: ")
    sorted_files: list[tuple[str, int]] = sort_files_by_occurrences(
        directory_path, key_string
    )
    print(
        "\nHere are the files with the key string contained. Their names are given in descending order of the number of times the key string occurred in the files:\n"
    )
    file: str
    occurrences: int
    for file, occurrences in sorted_files:
        print(f"{file}: {occurrences} occurrences")


if __name__ == "__main__":
    main()
