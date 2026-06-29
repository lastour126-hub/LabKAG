import argparse

import requests


def main() -> None:
    parser = argparse.ArgumentParser(description="Search LabKAG evidence.")
    parser.add_argument("query")
    parser.add_argument("--project-id", default="labkag_demo")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    args = parser.parse_args()

    response = requests.post(
        f"{args.base_url}/v1/evidence/search",
        json={"query": args.query, "project_id": args.project_id},
        timeout=30,
    )
    response.raise_for_status()
    print(response.text)


if __name__ == "__main__":
    main()
