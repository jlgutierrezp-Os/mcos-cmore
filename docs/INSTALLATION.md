# Installation

## From GitHub branch

```bash
git clone https://github.com/jlgutierrezp-Os/mcos-cmore.git
cd mcos-cmore
git checkout integration/mcos-transfer-v0-1-r
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m mcos.cli selfdebug
python -m unittest discover -s tests
```

## Smoke tests

```bash
python -m mcos.cli validate object examples/group_object.json
python -m mcos.cli validate relation examples/group_relation.json
python -m mcos.cli ingest examples/feed_source_package.json --dry-run
python -m mcos.cli feed-registry
python -m mcos.cli bootstrap-readiness
```

## Local graph write

```bash
python -m mcos.cli graph-add examples/group_object.json
python -m mcos.cli graph-edge examples/group_relation.json
python -m mcos.cli graph-export
```

## Do not use main yet

The `main` branch currently contains only a placeholder. Use the integration branch until human review promotes it.
