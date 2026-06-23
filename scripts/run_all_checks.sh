#!/usr/bin/env bash
set -euo pipefail
python -m mcos.cli selfdebug
python -m unittest discover -s tests
python -m mcos.cli validate object examples/group_object.json
python -m mcos.cli validate relation examples/group_relation.json
python -m mcos.cli ingest examples/feed_source_package.json --dry-run
python -m mcos.cli ingest examples/foundation_layer_seed.json --dry-run
python -m mcos.cli feed-registry
python -m mcos.cli bootstrap-readiness
