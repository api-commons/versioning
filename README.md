# Versioning

A machine-readable description of how an API is versioned — the scheme the version
string follows, where a consumer puts it on a request, which versions are currently
reachable, and what happens to the ones that are not.

This is the schema behind the [Versioning property](https://apicommons.org/common/versioning/)
in [API Commons](https://apicommons.org).

Versioning is documented in prose almost everywhere and expressed identically almost
nowhere. Every provider has a page about it; no two pages are the same shape. The point
of this schema is that a consumer — or an agent — can work out how to pin a version
without reading one.

## Artifacts

- **[versioning-json-schema.yml](versioning-json-schema.yml)** — the JSON Schema (2020-12).
- **[versioning-example-1.yml](versioning-example-1.yml)** — path-based sequential
  versioning with four versions in flight, one of them retired.
- **[versioning-example-2.yml](versioning-example-2.yml)** — the `Versioning` property
  envelope, showing date-pinned header versioning and vendor media-type versioning.
- **[validate.py](validate.py)** — validates any document against the schema.

## Using it

A declaration is an object:

```yaml
scheme: sequential      # semantic | calendar | date | sequential | custom | none
location: path          # path | header | query | media-type | subdomain | body
path_pattern: /v{version}
current: '3'
default: '2'
required: true
pinning: per-request    # per-request | per-account | per-key | none
supported:
  - version: '2'
    status: deprecated
    sunset: '2027-02-01'
  - version: '3'
    status: current
```

…or wrapped in the `Versioning` property envelope for an `apis.yml` index:

```yaml
- name: Versioning
  type: Versioning
  url: https://developers.example.com/versioning
  source_date: '2026-08-17'
  data:
    scheme: date
    location: header
    parameter: Example-Version
    current: '2026-08-01'
```

Only `scheme` and `location` are required. Four optional fields are worth filling in
anyway, because they are what consumers get wrong:

- **`default`** — what gets served when no version is sent. It is frequently *not*
  `current`, and the gap is where unversioned integrations quietly break.
- **`required`** — whether a request must carry a version at all. An unversioned request
  that silently rolls forward is a breaking change waiting for a release date.
- **`pinning`** — whether the version is chosen per request, per account, or per key.
  Stripe pins per account; most APIs pin per request; the two need different client code.
- **`breaking_change_definition_url`** — where the provider states what it *counts* as
  breaking. Without it, "we don't make breaking changes" is unfalsifiable.

`sunset` on a version should match the value the provider sends in the
[Sunset header](https://www.rfc-editor.org/rfc/rfc9745).

## Validating

```
pip install jsonschema pyyaml
python3 validate.py versioning-example-1.yml
```

## Support

Questions, corrections, and requests go in
[the issues](https://github.com/api-commons/versioning/issues).

## License

Two licenses, by kind of thing:

- **Artifacts** — the schemas, rulesets, fixtures, examples and API descriptions — are
  **[CC BY-NC-SA 4.0](LICENSE)** (Attribution–NonCommercial–ShareAlike).
- **Code** — the validator, test harness and packaging — is **[Apache-2.0](LICENSE-CODE)**.

API Commons licenses **artifacts** under CC BY-NC-SA 4.0 and **code** under Apache-2.0.

## Part of API Commons

A machine-readable building block from **[API Commons](https://apicommons.org)** — open specifications and schemas for the APIs you produce and consume. See all building blocks at **[apicommons.org](https://apicommons.org)** and the tools at **[apicommons.org/tools](https://apicommons.org/tools/)**.

**Related building blocks**
- [plans](https://github.com/api-commons/plans) — access plans, tiers, and pricing
- [rate-limits](https://github.com/api-commons/rate-limits) — the quotas an API enforces
- [starters](https://github.com/api-commons/starters) — the smallest correct version of each artifact
