import argparse

import requests


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload a PDF to LabKAG.")
    parser.add_argument("pdf_path")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    args = parser.parse_args()

    with open(args.pdf_path, "rb") as file:
        response = requests.post(
            f"{args.base_url}/v1/papers/upload",
            files={"file": (args.pdf_path, file, "application/pdf")},
            timeout=30,
        )
    response.raise_for_status()
    print(response.text)


if __name__ == "__main__":
    main()
