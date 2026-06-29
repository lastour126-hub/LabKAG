import argparse
import json
from pathlib import Path

import requests


def main() -> None:
    parser = argparse.ArgumentParser(description="Mock-ingest a PaperExtractionResult.")
    parser.add_argument("extraction_json")
    parser.add_argument("--project-id", default="labkag_demo")
    parser.add_argument("--confirm", action="store_true")
    parser.add_argument("--base-url", default="http://127.0.0.1:8000")
    args = parser.parse_args()

    paper_extraction = json.loads(Path(args.extraction_json).read_text(encoding="utf-8"))
    response = requests.post(
        f"{args.base_url}/v1/papers/ingest",
        json={
            "project_id": args.project_id,
            "paper_extraction": paper_extraction,
            "confirm": args.confirm,
        },
        timeout=30,
    )
    response.raise_for_status()
    print(response.text)


if __name__ == "__main__":
    main()
