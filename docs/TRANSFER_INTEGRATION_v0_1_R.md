# MCOS Transfer Integration v0.1-R

## Purpose

This branch integrates `MCOS_Project_Transfer_Package_v0_1_R` into `mcos-cmore` without replacing the local-first kernel.

## Decision

```json
{
  "core_replacement": false,
  "transfer_staged": true,
  "docs_promoted_to_review": true,
  "api_preview_added": true,
  "api_preview_status": "optional_not_core",
  "source_documents_imported": false,
  "external_apis_active": false,
  "paid_apis_active": false,
  "human_review_required": true
}
```

## Integration map

```text
MCOS_Project_Transfer_Package_v0_1_R/
├── 00_START_HERE              -> docs/transfers/.../00_START_HERE
├── 02_generated_specs          -> docs/specification/transfer_v0_1_R
├── 03_inferred_missing_specs   -> docs/inferred_specs/transfer_v0_1_R
├── 04_executable_bootstrap     -> apps/local_api_preview
├── 05_review_and_build         -> docs/transfers/.../05_review_and_build
└── 06_installation_notes       -> docs/transfers/.../06_installation_notes
```

## Non-imported by default

`01_source_documents/current_mounted` was inventoried but not imported into the public-ready repo by default.

## Human review gate

The integration is staged. Promotion to core requires explicit human decision.
