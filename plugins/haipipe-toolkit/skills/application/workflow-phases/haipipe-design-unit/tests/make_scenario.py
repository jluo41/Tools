"""Make non-sensitive forward-test inputs. Never uses a live release or Board."""
import argparse
from pathlib import Path
from test_unit import DesignUnitGateTest

parser = argparse.ArgumentParser()
parser.add_argument("directory", type=Path)
args = parser.parse_args()
owner = args.directory.resolve()
if owner.exists() and (not owner.is_dir() or any(owner.iterdir())):
    parser.error("forward-test directory must be absent or empty; never overwrite work")
owner.mkdir(parents=True, exist_ok=True)
case = DesignUnitGateTest()
case.owner = owner
case.approval = owner / "outline" / "release.md"
case.write(case.approval,
           "# Synthetic test fixture release\n"
           "The two written fixture commissions below are approved for testing only.\n"
           "Generate one respectful SMS, at most 160 Unicode code points, including "
           "{confirmation_link}. Independently review the supplied legacy-style "
           "candidate against the stricter configured cap. No sending or adoption.\n")
generation = case.ticket()
# A real, frozen manifest-backed fixture DU, deliberately inconsistent with
# a later stricter review criterion. Its provenance is explicitly synthetic.
fixture_ticket = case.ticket(10)
fixture_du = case.result(fixture_ticket)
review = case.ticket(2, "verify", [case.ref(fixture_du)], {
    "criteria": [{"id": "length", "kind": "max_chars", "value": 12},
                 {"id": "tone", "kind": "semantic",
                  "description": "Respectful, non-coercive language"}]})
print("owner:", owner)
print("generation:", generation)
print("verification:", review)
