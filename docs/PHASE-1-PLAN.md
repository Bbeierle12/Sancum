# SanctumGPT: Phase 1 - Ontology Consolidation

This document outlines the canonical data schema, tag lists, and migration procedures for SanctumGPT's data store.

---

## 1. Canonical Covenant Tags

This is the authoritative list of tags to be used in the `covenant_tags` field.

*   Atonement
*   Creation
*   Priesthood
*   Sabbath
*   Judgment
*   Mercy
*   Resurrection
*   Law
*   Grace
*   Covenant-Renewal
*   Kingship
*   Exile-Return
*   Temple
*   Wisdom
*   Prophecy

---

## 2. Canonical Emotion Codes

This is the authoritative list of codes for the `emotion_codes` field, grouped by category.

### Love / Joy
*   Love
*   Joy
*   Gratitude
*   Affection
*   Delight
*   Celebration

### Sorrow / Grief
*   Grief
*   Sorrow
*   Lament
*   Anguish
*   Despair

### Fear / Anxiety
*   Fear
*   Anxiety
*   Dread
*   Worry

### Anger / Conflict
*   Anger
*   Wrath
*   Contempt
*   Frustration
*   Conflict

### Peace / Hope
*   Hope
*   Peace
*   Comfort
*   Trust
*   Assurance
*   Confidence

### Awe / Reverence
*   Awe
*   Reverence
*   Wonder
*   Veneration

---

## 3. Migration and Extension Guidance

Follow this checklist when adding to or modifying your Sanctum data files.

*   **☐ File Naming**: Save your data in files like `sanctum_data_YYYYMMDD.yaml` to maintain versioned backups.
*   **☐ Tag Hygiene**: Only use tags and codes from the canonical lists in this document to ensure consistency.
*   **☐ YAML Syntax**: YAML is sensitive to indentation. Use spaces, not tabs, and double-check alignment. Online YAML linters can be a helpful tool.
*   **☐ Run Validation Often**: Before saving your work or after a large number of additions, run the validation script: `python scripts/validate_schema.py <path_to_your_data_file>.yaml`.
*   **☐ Backup Before Editing**: Always back up your data file before making significant changes.
*   **☐ Extending the Schema**: To add a new field, first update `docs/sanctum_schema.yaml` and the Pydantic models in `scripts/validate_schema.py` before adding it to your data files.
