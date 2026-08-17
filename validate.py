#!/usr/bin/env python3
"""Validate a document against this repo's JSON Schema.

Usage:
  python3 validate.py versioning-example-1.yml [more.yml ...]

Exits non-zero if any document fails, so it can gate a pipeline.
"""

import glob
import os
import sys

try:
    import yaml
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("Requires pyyaml and jsonschema:  pip install jsonschema pyyaml")

HERE = os.path.dirname(os.path.abspath(__file__))


def load_schema():
    matches = glob.glob(os.path.join(HERE, "*-json-schema.yml"))
    if len(matches) != 1:
        sys.exit(f"Expected exactly one *-json-schema.yml in {HERE}, found {len(matches)}")
    with open(matches[0]) as f:
        return yaml.safe_load(f)


def errors_for(schema, doc):
    return sorted(
        Draft202012Validator(schema).iter_errors(doc),
        key=lambda e: list(e.absolute_path),
    )


def best_branch_errors(schema, doc):
    """Report errors from the oneOf branch the document came closest to matching.

    Validating against the oneOf itself yields only "is not valid under any of the
    given schemas", which hides the actual mistake. Trying each branch and keeping
    the one with the fewest errors means every message points at a real field.
    """
    branches = schema.get("oneOf")
    if not branches:
        return errors_for(schema, doc)

    shared = {k: v for k, v in schema.items() if k in ("$schema", "$defs")}
    attempts = [errors_for({**shared, **branch}, doc) for branch in branches]
    return min(attempts, key=len)


def validate(path, schema):
    with open(path) as f:
        doc = yaml.safe_load(f)

    errors = best_branch_errors(schema, doc)
    if not errors:
        count = len(doc) if isinstance(doc, list) else 1
        print(f"PASS  {path}  ({count} entries)")
        return True

    print(f"FAIL  {path}  ({len(errors)} errors)")
    for e in errors:
        where = "/".join(str(p) for p in e.absolute_path) or "(root)"
        print(f"      {where}: {e.message}")
    return False


def main(argv):
    if not argv:
        sys.exit(__doc__)

    schema = load_schema()
    Draft202012Validator.check_schema(schema)

    ok = all([validate(p, schema) for p in argv])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
