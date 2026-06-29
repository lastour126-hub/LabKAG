import argparse

import requests


def main() -> None:
    parser = argparse.ArgumentParser(description="Query LabKAG literature knowledge.")
    parser.add_argument("question")
    parser.add_argument("--project-id", default="labkag_demo")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    args = parser.parse_args()

    response = requests.post(
        f"{args.base_url}/v1/literature/query",
        json={"question": args.question, "project_id": args.project_id},
        timeout=30,
    )
    response.raise_for_status()
    print(response.text)


if __name__ == "__main__":
    main()
