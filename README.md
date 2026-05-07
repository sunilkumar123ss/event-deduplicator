# TTL event deduplicator

Reject repeated event IDs within a bounded first-seen retention window.

Educational implementation with synthetic examples.

## Run

Python 3.9 or newer; standard library only. From this directory:

```sh
python3 main.py
python3 main.py --help
python3 -m unittest -v
```

The default example uses synthetic data and needs no credentials, installation, or network connection. The script also works by absolute path from another working directory.

## Behavior

An accepted ID remains reserved until first-seen time plus TTL. Duplicates do not extend retention. Expiration is inclusive at the boundary. When the live capacity is full, new IDs are rejected with an explicit error rather than silently evicting deduplication evidence.

## Use in Python

```python
from main import Deduplicator

seen = Deduplicator(ttl=60, capacity=1000)
assert seen.accept('example-event', now=0) is True
assert seen.accept('example-event', now=30) is False
assert seen.accept('example-event', now=60) is True
```

## Design limits

In-memory ID tracking with monotonic caller time, scoped to one process. It does not atomically couple acceptance to a database side effect. A duplicate arriving after TTL is accepted again. Real consumers need durable idempotency records when their side effects require them.

## Verification

The unit tests cover successful operations, failure paths, and invariants. These are local correctness checks, not production performance or security certification.

## Repository checks

```sh
python3 verify.py
```

This runs the isolated test suite, synthetic example, and CLI help. The included GitHub Actions workflow repeats these checks when the repository is published. No hosted CI result is claimed by the local verification report.
