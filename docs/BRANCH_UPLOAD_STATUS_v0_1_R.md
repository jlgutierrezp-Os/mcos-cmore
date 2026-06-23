# Branch Upload Status v0.1-R

Branch: `integration/mcos-transfer-v0-1-r`

## Current state

The branch exists and is ahead of `main`.

Uploaded so far:

- `registry/transfer_integration_decision_v0_1_R.json`
- `docs/TRANSFER_INTEGRATION_v0_1_R.md`
- `docs/TRANSFER_PROMOTION_PLAN_v0_1_R.md`
- `apps/local_api_preview/README.md`
- `docs/transfers/MCOS_Project_Transfer_Package_v0_1_R/SOURCE_DOCUMENTS_NOT_IMPORTED.md`

## Source package status

The original transfer ZIP has not been fully unpacked into GitHub by this connector step.

Reason:

- avoid direct public upload of unreviewed source material;
- keep source documents private by default;
- preserve staged integration instead of replacing core;
- upload must continue in reviewed batches or by local git push.

## Next reviewed upload batches

1. Core kernel files.
2. Tests and examples.
3. Foundation layer docs and registry.
4. Feeding and zero-distillation docs.
5. Inferred specs.
6. Optional local API preview files.
7. Transfer inventory and reports.

## Human gate

Do not merge into `main` until the branch has been reviewed and the human operator approves promotion.
