# Runtime Contract

Use `scripts/context_eval.py` when evaluation evidence needs deterministic validation, normalization, filesystem identity, or matched-pair arithmetic. The runtime is standard-library-only Python 3 and deliberately stops before semantic adjudication.

## Commands

```text
python3 scripts/context_eval.py init EVALUATION_ID [--root ROOT] [--reuse]
python3 scripts/context_eval.py validate INPUT [--contract VERSION]
python3 scripts/context_eval.py normalize NATIVE.jsonl --attempt-id ID (--blobs-dir DIR | --workspace WORKSPACE --artifact-slug SLUG) [--inline-limit-bytes N]
python3 scripts/context_eval.py snapshot ROOT [--exclude RELATIVE_PATH ...] [--workspace WORKSPACE --artifact-slug SLUG --label LABEL]
python3 scripts/context_eval.py evaluate INPUT [--workspace WORKSPACE]
```

All successful commands emit one canonical JSON value to stdout: UTF-8, sorted object keys, compact separators, finite numbers only, and one trailing newline. Diagnostics go to stderr.

Exit codes are stable:

- `0`: success;
- `2`: command-line usage error;
- `3`: filesystem or text I/O error;
- `4`: malformed JSON, contract violation, invalid path, or invalid normalization option;
- `5`: an evaluation is contract-valid but cannot be computed without unsupported inference;
- `6`: unexpected internal failure.

## Evaluation Workspaces

`init` creates `.context-evaluation/YYYY-MM-DD/EVALUATION_ID/` at the nearest ancestor containing `.git`, or at the requested/current directory when no VCS marker exists. The strict `ctxeval.workspace.v1` manifest contains only `schemaVersion`, `evaluationId`, `localDate`, and timezone-aware `createdAt`; it never records host paths. IDs, artifact slugs, and labels are conservative lowercase ASCII slugs (maximum 64 characters). Initialization is exclusive. `--reuse` is read-only and succeeds only when the existing manifest, date/ID path identity, and required `subject/` and `evaluator/` directories match exactly.

Workspace publication is descriptor-relative and no-follow from a trusted filesystem anchor through every caller-supplied path component. A workspace handle retains the validated evaluation, subject, and evaluator directory descriptors for the entire operation: normalization and snapshots derive only from the retained subject descriptor, while report publication uses the retained evaluator descriptor. Publication therefore never validates a child pathname and later reopens it. Arbitrary absolute and relative workspace paths are supported only when every ancestor is a real directory. Manifest identity must match the actual `.context-evaluation/LOCAL_DATE/EVALUATION_ID` path components.

Fixed artifacts are immutable: normalization safely creates or reuses `subject/attempts/SLUG/`, exclusively claims its `normalized/` slot, then publishes `events.jsonl` and derived content-addressed `blobs/`; snapshots publish `subject/attempts/SLUG/trees/LABEL.json`; evaluation publishes `evaluator/report.json`. This permits `trees/` and `normalized/` to coexist for one artifact slug. Any existing full or partial `normalized/` slot is occupied. `--attempt-id` and `--inline-limit-bytes` are validated before workspace mutation. A normalization failure deliberately leaves its claimed `normalized/` slot occupied and it cannot be reused by the same or a different semantic attempt ID. The semantic `--attempt-id` is evidence metadata and is intentionally independent of the filesystem `--artifact-slug`. Computation and validation finish before canonical/text publication, and publication finishes before stdout; publication failure therefore emits no stdout. Existing verified content-addressed blobs may be reused within the claimed slot, but fixed artifacts cannot be replaced. The runtime has no force mode, recursive deletion, index, workspace ignore semantics, or in-project oracle directory.

Add `/.context-evaluation/` to project ignore configuration explicitly when appropriate; `init` never edits `.gitignore`. When snapshotting a project containing the workspace, pass `--exclude .context-evaluation` explicitly. A workspace and ignore rule are organizational and provenance controls, not subject/evaluator or subject/oracle isolation. Keep hidden acceptance and oracle material outside the evaluated project and expose only adjudicated results/evidence permitted by the experiment design.

## Versioned Boundaries

- `ctxeval.workspace.v1`: strict host-path-free workspace identity and local timestamp metadata.
- `ctxeval.input.v1`: attempts, their unconditional outcomes, ordered gate inputs, native/derived/adjudicated metrics, and explicit pair membership.
- `ctxeval.event.v1`: line-preserving normalized events. Each event records `lineTerminator` as `none`, `lf`, or `crlf`; splitting occurs only on LF, so bare CR remains payload content. Valid JSON scalars are preserved exactly, including an inline JSON `null`; `payloadBlob` distinguishes blob-backed invalid or oversized records from inline null. Invalid UTF-8, malformed JSON, non-finite JSON constants, and payloads over the inline limit become content-addressed blobs rather than disappearing. Event IDs are unique across the stream; native IDs are reserved before deterministic synthesized-ID probing.
- `ctxeval.tree.v1`: sorted regular-file and symlink entries with byte counts and SHA-256 identities. Exclusions use normalized relative POSIX paths and segment-aware containment. Descriptor-relative, no-follow traversal rejects detected identity or content mutation; callers must provide a stable tree and retry if concurrent mutation is reported.
- `ctxeval.report.v1`: unconditional attempt results and explicitly declared pair results.

Contracts reject unknown fields, including nested report fields. Metric integers are restricted to the interoperable safe JSON range `[-9007199254740991, 9007199254740991]`; floats must be finite. The CLI configures parsing to reject larger integer literals, including extremely long literals, as contract errors before evaluation. Missing observations are represented as `value: null` plus a non-null `missingReason`; zero remains a measured zero. Pass/fail gates and present metric values require at least one evidence reference. Unknown gates and missing metrics may preserve an empty evidence list when no reference exists. Existing blob paths are accepted only when they are non-symlink regular files whose length, digest, and bytes match. Pre-open, opened-descriptor, and post-read pathname identity (device, inode, size, and modification time) must remain stable; replacement during verification is rejected. The blob root itself must be a non-symlink directory and publication remains anchored to its verified open directory descriptor; integrity failures are deterministic contract errors.

## Evaluation Semantics

Attempts retain every outcome: `success`, `failed`, `refused`, `timed_out`, `permission_denied`, or `infrastructure_failed`. Resource eligibility requires `success` and a `pass` at every noncompensable gate, in this order:

1. `telemetry`
2. `correctness`
3. `safety`
4. `evidenceCoverage`

Pairs are evaluated only when explicitly listed and both attempts are resource-eligible. A metric is comparable only when present for both attempts, measured natively, non-missing, and identical in unit and non-null `compatibilityKey`. The runtime reports baseline, treatment, and signed delta; it does not name a winner, create a score, normalize unlike units, infer absent values, judge relevance, or decide causal usefulness.

Task acceptance, safety interpretation, evidence sufficiency, semantic relevance, rubric application, causal claims, and rollout decisions stay outside the runtime. Record those judgments as gate statuses or adjudicated metrics with evidence before evaluation. See `evidence-model.md` for provenance and exposure semantics, `annotation-guide.md` for adjudication boundaries, and `experiment-design.md` for matching and estimands.
