#!/usr/bin/env python3
"""
Shared utilities for the Recurrent Glioma Multi-Omics Explorer data pipeline.
"""

import json
import logging
import re
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Keyword sets for recurrent glioma relevance detection
# ---------------------------------------------------------------------------

RECURRENCE_TERMS = [
    "recurrent", "recurrence", "relapsed", "relapse",
    "progressive", "progression",
    "second surgery", "re-operation", "reoperation",
    "longitudinal", "paired primary", "matched primary",
    "tumor evolution", "tumour evolution",
    "clonal evolution", "temporal evolution",
    "initial and recurrent", "primary and recurrent",
    "de novo and recurrent", "treatment-resistant",
    "post-treatment", "post treatment",
    "transformed", "malignant transformation",
    "hypermutation", "acquired resistance",
]

GLIOMA_TERMS = [
    "glioma", "glioblastoma", "gbm",
    "astrocytoma", "oligodendroglioma",
    "diffuse glioma", "high grade glioma", "high-grade glioma",
    "low grade glioma", "low-grade glioma",
    "idh mutant", "idh-mutant",
    "grade iv glioma", "grade 4 glioma",
]

# ---------------------------------------------------------------------------
# Data type classification rules (order matters: more specific first)
# ---------------------------------------------------------------------------

DATA_TYPE_RULES = [
    ("scRNA-seq", [
        "single-cell rna", "single cell rna", "single-cell transcriptom",
        "single cell transcriptom", "scrna-seq", "scrna seq", "scrnaseq",
        "10x genomics", "10x chromium", "drop-seq", "dropseq",
        "smart-seq", "smartseq", "cel-seq", "celseq", "indrops", "sci-rna",
    ]),
    ("snRNA-seq", [
        "single-nucleus rna", "single nucleus rna", "single-nuclei rna",
        "single nuclei rna", "snrna-seq", "snrna seq", "snrnaseq",
    ]),
    ("spatial transcriptomics", [
        "spatial transcriptom", "spatially resolved transcriptom", "spatial rna",
        "visium", "10x visium", "slide-seq", "slideseq", "merfish",
        "seqfish", "stereo-seq", "dbit-seq", "hdst", "cosmx", "xenium",
    ]),
    ("scATAC-seq", [
        "single-cell atac", "single cell atac", "single-nucleus atac",
        "single nucleus atac", "scatac-seq", "scatac seq", "scatacseq",
        "snatac-seq", "snatac seq", "snatac",
    ]),
    ("ATAC-seq", ["atac-seq", "atac seq", "atacseq"]),
    ("methylation array", [
        "methylation profiling by array", "450k", "epic array",
        "infinium", "methylation array", "dna methylation",
        "methylation profiling",
    ]),
    ("WES/WGS", [
        "whole exome", "whole genome sequencing", "wes ", "wgs ",
        "exome sequencing", "genome variation profiling", "targeted sequencing",
        "panel sequencing", "somatic mutation",
    ]),
    ("proteomics", [
        "proteom", "mass spectrometry", "tmt labeling", "itraq",
        "label-free quantification", "phosphoproteom",
    ]),
    ("bulk RNA-seq", [
        "rna-seq", "rna seq", "rnaseq", "mrna-seq", "mrna seq",
        "transcriptome sequencing",
        "expression profiling by high throughput sequencing",
    ]),
    ("microarray", [
        "expression profiling by array", "microarray", "gene chip",
        "affymetrix", "agilent",
    ]),
]

TRANSCRIPTOME_SPECIFIC_TYPES = {"scRNA-seq", "snRNA-seq", "spatial transcriptomics"}


def normalize_organism(org_str):
    """Normalize organism names: sort multi-organism entries alphabetically."""
    if not org_str:
        return ""
    parts = [p.strip() for p in org_str.replace(";", "; ").split("; ") if p.strip()]
    parts = sorted(set(parts))
    return "; ".join(parts)


def deduplicate_datasets(datasets):
    """Remove duplicate datasets by id, keeping the first occurrence."""
    seen = set()
    unique = []
    for ds in datasets:
        ds_id = ds.get("id", "")
        if ds_id and ds_id not in seen:
            seen.add(ds_id)
            unique.append(ds)
        elif not ds_id:
            # Keep entries without an id (should not happen but be safe)
            unique.append(ds)
    return unique


def validate_dataset(ds):
    """Validate that a dataset has the minimum required fields.

    Returns a tuple of (is_valid, list_of_missing_fields).
    """
    required_fields = ["id", "source", "title"]
    missing = [f for f in required_fields if not ds.get(f)]
    return len(missing) == 0, missing


def save_data(datasets, filepath):
    """Save datasets list to a JSON file with proper encoding."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    filepath.write_text(
        json.dumps(datasets, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    logger.info("Saved %d datasets to %s", len(datasets), filepath)


def load_existing_data(filepath):
    """Load existing JSON data from file. Returns empty list if file missing."""
    filepath = Path(filepath)
    if filepath.exists():
        try:
            data = json.loads(filepath.read_text(encoding="utf-8"))
            logger.info("Loaded %d existing datasets from %s", len(data), filepath)
            return data
        except (json.JSONDecodeError, OSError) as exc:
            logger.warning("Failed to load existing data from %s: %s", filepath, exc)
    return []


def is_recurrent_glioma(title, summary):
    """Check if a dataset is related to recurrent glioma using keyword matching.

    Both a recurrence term AND a glioma term must appear in the combined text.
    """
    combined = f"{title} {summary}".lower()

    has_recurrence = any(term in combined for term in RECURRENCE_TERMS)
    has_glioma = any(term in combined for term in GLIOMA_TERMS)

    return has_recurrence and has_glioma


def classify_data_types(title, summary, overall_design="", geo_data_type=""):
    """Classify data types from text fields. Returns a list of type strings."""
    combined = " ".join([
        title or "",
        summary or "",
        overall_design or "",
        geo_data_type or "",
    ]).lower()

    matched = []

    # Context-based detection for single-cell / single-nucleus RNA
    has_sc_rna = (
        ("single-cell" in combined or "single cell" in combined)
        and any(tok in combined for tok in ["transcriptom", "gene expression", "rna"])
    )
    has_sn_rna = (
        any(tok in combined for tok in [
            "single-nucleus", "single nucleus", "single-nuclei", "single nuclei",
        ])
        and any(tok in combined for tok in ["transcriptom", "gene expression", "rna"])
    )

    if has_sc_rna:
        matched.append("scRNA-seq")
    if has_sn_rna:
        matched.append("snRNA-seq")

    for label, keywords in DATA_TYPE_RULES:
        if any(kw in combined for kw in keywords):
            if label not in matched:
                matched.append(label)

    # Deduplicate: scATAC-seq supersedes ATAC-seq
    if "scATAC-seq" in matched and "ATAC-seq" in matched:
        matched.remove("ATAC-seq")

    # If specific transcriptome type matched, remove generic bulk RNA-seq
    if "bulk RNA-seq" in matched and any(t in matched for t in TRANSCRIPTOME_SPECIFIC_TYPES):
        matched.remove("bulk RNA-seq")

    return matched


def make_dataset_entry(
    *,
    id,
    source,
    accession="",
    title="",
    organism="Homo sapiens",
    data_types=None,
    sample_count=0,
    recurrent_sample_count=None,
    tumor_subtypes=None,
    molecular_markers=None,
    treatment_info="",
    summary="",
    contributors="",
    institution="",
    country="",
    publication_date="",
    pubmed_ids=None,
    source_url="",
    last_updated=None,
):
    """Create a dataset entry conforming to the unified schema."""
    return {
        "id": id,
        "source": source,
        "accession": accession or id,
        "title": title,
        "organism": organism,
        "data_types": data_types or [],
        "sample_count": sample_count,
        "recurrent_sample_count": recurrent_sample_count,
        "tumor_subtypes": tumor_subtypes or [],
        "molecular_markers": molecular_markers or [],
        "treatment_info": treatment_info,
        "summary": summary,
        "contributors": contributors,
        "institution": institution,
        "country": country,
        "publication_date": publication_date,
        "pubmed_ids": pubmed_ids or [],
        "source_url": source_url,
        "last_updated": last_updated or datetime.now().strftime("%Y-%m-%d"),
    }
