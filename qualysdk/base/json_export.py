from json import dump


def write_json(data: dict, output: str) -> None:
    with open(output, "w") as f:
        dump(data, f, indent=2)
    print(f"Data written to {output}.")
