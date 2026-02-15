"""
Docstring for selection.populate_verses
"""


# Note: \b-hearing\bible-data\corpus\eng-engkjv.txt for kjv
def copy_all_verses(src_path, out_path):
    src_path = r"bible-data\\corpus\\eng-engkjvcpb.txt"
    out_path = r"bible-data\\corpus\\eng-engkjv.txt"
    with open(src_path, "rb") as src:
        with open(out_path, "wb") as out:
            for _ in range(31170):
                out.write(src.readline())


def populate_verses(version: str):
    pass
