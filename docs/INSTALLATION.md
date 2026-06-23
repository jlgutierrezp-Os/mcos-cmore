# Installation

## Main branch

MCOS/C-MORE v0.1-R is now installed from `main`.

```bash
git clone https://github.com/jlgutierrezp-Os/mcos-cmore.git
cd mcos-cmore
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m mcos.cli selfdebug
python -m unittest discover -s tests
bash scripts/run_all_checks.sh
```

## Smoke tests

```bash
python -m mcos.cli validate object examples/group_object.json
python -m mcos.cli validate relation examples/group_relation.json
python -m mcos.cli ingest examples/feed_source_package.json --dry-run
python -m mcos.cli ingest examples/foundation_layer_seed.json --dry-run
python -m mcos.cli feed-registry
python -m mcos.cli bootstrap-readiness
```

## Local graph write

```bash
python -m mcos.cli graph-add examples/group_object.json
python -m mcos.cli graph-edge examples/group_relation.json
python -m mcos.cli graph-export
```

## Status

PR #1 was squash-merged and `main` now contains the MCOS/C-MORE v0.1-R bootstrap.
