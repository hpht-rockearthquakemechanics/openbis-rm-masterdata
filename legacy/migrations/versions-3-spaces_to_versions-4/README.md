# V3 spaces → V4 external-vocabulary crosswalk

## Status

**Experimental archival evidence.** This directory preserves an attempted
crosswalk from selected V3 vocabulary terms to external vocabulary references
considered during the V4 transition. It is not an OpenBIS import package, an
approved semantic migration, or an executable production workflow.

Nothing in this directory belongs in `versions-4/datamodel/` or is to be
imported automatically into an OpenBIS instance.

## Purpose and boundaries

The bundle records a limited V3-spaces → V4 investigation:

- V3 inputs are derived from
  `../../versions-3-spaces/datamodel/metadata-model-rockmechanics_V3_spaces.xlsx`
  and `../../versions-3-spaces/datamodel/msl-dictionaries.xlsx`.
- Candidate target vocabularies are preserved under
  `external_vocabularies/openbis_reference_vocabularies/`.
- The bundle maps labels; it does not transform object types, properties,
  datasets, collections, or existing OpenBIS data.
- The external references are migration resources, not proof that the
  corresponding terms are part of the V4 master-data model.

The V3 source export contains 22 vocabulary blocks with 2,843 terms. This
attempt covers only these six source groups (611 terms):

| V3 source group | Candidate target group(s) | Exact-label matches | Excluded |
| --- | --- | ---: | ---: |
| `MSL_ROCK` | `MSL_ROCK` | 180 / 204 | 24 |
| `UNITS` | `QUDT_UNIT` | 88 / 111 | 23 |
| `PHYSICALQUANTITIES` | `QUDT_QUANTITYKIND` | 78 / 103 | 25 |
| `ROCKS` | `BGS_ROCKNAME` | 84 / 182 | 98 |
| `FLUIDS` | `SWEET_STATE_PHYS` | 2 / 3 | 1 |
| `ARTIFICIALMATERIALS` | `SWEET_MATR_CORE`, `SWEET_MATR_IND` | 1 / 8 | 7 |

Across the selected scope, 433 of 611 unique V3 terms (70.9%) have an
exact case-insensitive label match; 178 are excluded from the selected target
vocabularies. The mapped reports contain 439 rows because some labels have
more than one target match.

The remaining 16 V3 vocabulary blocks (2,232 terms) are outside this
experiment's scope.

## Contents

```text
external_vocabularies/
  before_mapping/                 V3 vocabulary export and its construction notebook
  openbis_reference_vocabularies/ candidate target vocabulary CSVs and merge notebook
  after_mapping/                  per-group mapped and excluded reports
  download_external_vocabularies.ipynb
                                  source-acquisition notebook (network-dependent)
  environment.yml                 recorded notebook environment
```

The bundle currently contains 42 CSV files, four notebooks, and one
environment definition.

## Source inventory and provenance

This README is the human-readable inventory for the archived external
resources. The notebook source code and the local filenames are the evidence
recorded here; this section does not infer a redistribution licence from public
availability.

| Local archived material | Recorded upstream reference | Version or pinning recorded locally | Role in this bundle |
| --- | --- | --- | --- |
| `qudt_units_unique_v3.1.10.csv`, `qudt_quantitykinds_v3.1.10.csv` | `http://qudt.org/3.1.10/vocab/unit` and `http://qudt.org/3.1.10/vocab/quantitykind` | QUDT `3.1.10`, versioned URLs | Candidate targets for `UNITS` and `PHYSICALQUANTITIES`. |
| `sweet_materials_industrial_v3.6.0.csv`, `sweet_physical_states_v3.6.0.csv` | `https://raw.githubusercontent.com/ESIPFed/sweet/master/src/matrIndustrial.ttl` and `https://raw.githubusercontent.com/ESIPFed/sweet/master/src/statePhysical.ttl` | Local filenames identify `3.6.0`; the recorded notebook URLs point to the upstream `master` branch rather than an immutable tag | Candidate targets for `ARTIFICIALMATERIALS` and `FLUIDS`. |
| `bgs_rock_name_v2.5.csv` | `https://vocab.bgs.ac.uk/v/vocab/rthmtrlclss:RockName` | Local filename identifies `2.5` | Candidate target for `ROCKS`. |
| `msl_combined_editor_v1.4.csv` | `https://raw.githubusercontent.com/UtrechtUniversity/msl_vocabularies/main/vocabularies/combined/editor/1.4/editor_1-4.json` | MSL editor `1.4` | Source for the locally split `MSL_*.csv` reference vocabularies, including `MSL_ROCK`. |
| `before_mapping/metadata-model-rockmechanics_V3_spaces_vocabularies.csv` | Local V3 workbook inputs named above | Derived locally from the preserved V3 workbooks | Legacy-side vocabulary export. |
| `openbis_reference_vocabularies/*.csv`, `external_dictionaries_merged.csv` | The local source CSVs listed above | Derived locally by `merging.ipynb` | Consolidated candidate target reference. |
| `after_mapping/*/report_1toN_*.csv` | The two local consolidated exports | Derived locally by `mapping.ipynb` | Candidate exact-label mapping and exclusion evidence. |

The source URLs were public and accessible when this bundle was assembled.
Before publication, redistribution outside this archive, or production use,
confirm the applicable licence, attribution, retrieval date, and any required
source-specific notice. The bundle remains archival evidence until then.

## Method recorded by the notebooks

1. `before_mapping/merge_v3_dictionaries.ipynb` combines the V3 workbook
   vocabulary sheets into `metadata-model-rockmechanics_V3_spaces_vocabularies.csv`.
2. `openbis_reference_vocabularies/merging.ipynb` creates a single target
   reference file from the selected local CSV files.
3. `after_mapping/mapping.ipynb` extracts one V3 group and one or more target
   groups, lower-cases `Label`, and performs an exact label join.
4. The notebook writes `report_1toN_mappati.csv` and
   `report_1toN_esclusi.csv` for each selected source group.

The `1-to-N` wording means that a single V3 label can match multiple target
records. It is not evidence that every such target is an approved replacement.

## Limitations and handling rules

- Matching is exact after lower-casing only. It does not resolve synonyms,
  spelling variants, unit conversions, hierarchy changes, or semantic
  equivalence.
- A match must be reviewed before it is used as a migration decision;
  an excluded term is not necessarily invalid or obsolete.
- The reports are candidate crosswalk evidence, not authoritative mappings.
- Preserve the notebooks and CSVs as historical resources; do not execute
  them automatically or in CI.
- `download_external_vocabularies.ipynb` accesses network resources. Do not
  run it without explicit authorization and a separate provenance review.
- Public accessibility and the recorded source URLs do not by themselves prove
  redistribution rights. Confirm licences and attribution before publication,
  redistribution outside this archive, or production use.
- Keep raw model reports, comparisons, and rendered report artifacts outside
  this directory under the ignored local `reports/` workflow.

## Before any future migration use

1. Complete and review the source inventory above with licences, attribution,
   retrieval dates, and any source-specific notices required for the intended
   use.
2. Review all one-to-many matches and excluded terms with domain owners.
3. Produce a separately versioned, human-approved mapping if a real migration
   is required.
4. Test any approved mapping in a non-production environment; OpenBIS imports
   remain manual and require their own authorization.
