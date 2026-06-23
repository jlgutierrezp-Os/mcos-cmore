# Pull Request

## Summary

Describe the change.

## Scope

- [ ] Core kernel
- [ ] Ingestion
- [ ] Distillation
- [ ] Foundation Layer
- [ ] Documentation
- [ ] Tests
- [ ] Future adapter boundary

## Checks

- [ ] `python -m unittest discover -s tests`
- [ ] `python -m mcos.cli selfdebug`
- [ ] `bash scripts/run_all_checks.sh`

## Safety

- [ ] No credentials
- [ ] No private records
- [ ] No paid API activation
- [ ] No external API activation
- [ ] Human review gate preserved

## Decision requested

- [ ] accept
- [ ] revise
- [ ] defer
- [ ] reject
- [ ] promote_to_core
