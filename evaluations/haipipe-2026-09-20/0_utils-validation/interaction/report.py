import json
import sys


def build_report(values):
    average = sum(values) / len(values) if values else None
    return {"count": len(values), "average": average}


if __name__ == "__main__":
    values = json.loads(sys.argv[1])
    print(json.dumps(build_report(values)))
