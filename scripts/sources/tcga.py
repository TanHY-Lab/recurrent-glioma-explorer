#!/usr/bin/env python3
"""
TCGA data source fetcher for recurrent glioma datasets.

Uses the GDC (Genomic Data Commons) API to query TCGA-GBM and TCGA-LGG
projects and extract information about recurrent/progressive cases.
"""

import logging

import requests

from scripts.utils import make_dataset_entry

logger = logging.getLogger(__name__)

GDC_API = "https://api.gdc.cancer.gov"
HTTP_SESSION = requests.Session()
HTTP_SESSION.headers.update({"User-Agent": "RecurrentGliomaExplorer/1.0"})

TCGA_PROJECTS = ["TCGA-GBM", "TCGA-LGG"]


def _query_gdc_project(project_id):
    """Query GDC for project-level case and data type information."""
    # Fetch project summary
    try:
        resp = HTTP_SESSION.get(
            f"{GDC_API}/projects/{project_id}",
            params={
                "expand": "summary,summary.data_categories,summary.experimental_strategies",
            },
            timeout=20,
        )
        if resp.status_code != 200:
            logger.warning("GDC project query for %s returned status %d", project_id, resp.status_code)
            return None
        return resp.json().get("data", {})
    except Exception as exc:
        logger.warning("GDC project query for %s failed: %s", project_id, exc)
        return None


def _count_recurrent_cases(project_id):
    """Count cases with recurrent/progressive disease in a TCGA project."""
    filters = {
        "op": "and",
        "content": [
            {
                "op": "=",
                "content": {"field": "project.project_id", "value": project_id},
            },
            {
                "op": "in",
                "content": {
                    "field": "diagnoses.tissue_or_organ_of_origin",
                    "value": ["Brain", "brain"],
                },
            },
        ],
    }

    # Query for recurrent sample types
    recurrent_filters = {
        "op": "and",
        "content": [
            {
                "op": "=",
                "content": {"field": "project.project_id", "value": project_id},
            },
            {
                "op": "in",
                "content": {
                    "field": "samples.sample_type",
                    "value": [
                        "Recurrent Tumor",
                        "Recurrent Blood Derived Cancer - Bone Marrow",
                        "Recurrent Blood Derived Cancer - Peripheral Blood",
                    ],
                },
            },
        ],
    }

    try:
        import json

        resp = HTTP_SESSION.post(
            f"{GDC_API}/cases",
            json={
                "filters": recurrent_filters,
                "size": 0,
                "from": 0,
            },
            timeout=20,
        )
        if resp.status_code == 200:
            data = resp.json().get("data", {})
            pagination = data.get("pagination", {})
            return pagination.get("total", 0)
    except Exception as exc:
        logger.warning("GDC recurrent case count for %s failed: %s", project_id, exc)

    return None


def _extract_data_types(project_data):
    """Extract data types from GDC project summary."""
    data_types = []
    summary = project_data.get("summary", {})

    strategies = summary.get("experimental_strategies", [])
    strategy_map = {
        "RNA-Seq": "bulk RNA-seq",
        "WXS": "WES/WGS",
        "WGS": "WES/WGS",
        "Genotyping Array": "microarray",
        "Methylation Array": "methylation array",
        "miRNA-Seq": "bulk RNA-seq",
        "ATAC-Seq": "ATAC-seq",
    }

    for strategy in strategies:
        name = strategy.get("experimental_strategy", "")
        mapped = strategy_map.get(name, name)
        if mapped and mapped not in data_types:
            data_types.append(mapped)

    return data_types


def _build_tcga_entry(project_id, project_data, recurrent_count):
    """Build a unified dataset entry for a TCGA project."""
    summary_info = project_data.get("summary", {})
    case_count = summary_info.get("case_count", 0)
    data_types = _extract_data_types(project_data)

    if project_id == "TCGA-GBM":
        title = "TCGA Glioblastoma Multiforme (TCGA-GBM)"
        subtypes = ["GBM"]
        description = (
            "The Cancer Genome Atlas Glioblastoma Multiforme project includes multi-omics "
            "profiling of GBM tumors. Contains a subset of recurrent tumor samples with "
            "whole-exome sequencing, RNA-seq, methylation array, and copy number data. "
            "A cornerstone resource for GBM genomics research."
        )
    else:
        title = "TCGA Low Grade Glioma (TCGA-LGG)"
        subtypes = ["Astrocytoma", "Oligodendroglioma", "Oligoastrocytoma"]
        description = (
            "The Cancer Genome Atlas Low Grade Glioma project includes comprehensive "
            "molecular profiling of WHO grade II-III diffuse gliomas. Contains IDH-mutant "
            "and IDH-wildtype cases with some recurrent samples."
        )

    return make_dataset_entry(
        id=f"TCGA_{project_id}",
        source="TCGA",
        accession=project_id,
        title=title,
        organism="Homo sapiens",
        data_types=data_types,
        sample_count=case_count,
        recurrent_sample_count=recurrent_count,
        tumor_subtypes=subtypes,
        molecular_markers=["IDH1", "IDH2", "MGMT", "TERT", "ATRX", "TP53", "EGFR", "PTEN"],
        treatment_info="Variable; see GDC portal for case-level treatment data",
        summary=description,
        contributors="The Cancer Genome Atlas Research Network",
        institution="NCI / NHGRI",
        country="USA",
        publication_date="2008-01-01",
        pubmed_ids=["23629348", "26061751"] if project_id == "TCGA-GBM" else ["26061373"],
        source_url=f"https://portal.gdc.cancer.gov/projects/{project_id}",
    )


# ---------------------------------------------------------------------------
# Fallback curated metadata when GDC API is unavailable
# ---------------------------------------------------------------------------

TCGA_FALLBACK = [
    {
        "id": "TCGA_TCGA-GBM",
        "source": "TCGA",
        "accession": "TCGA-GBM",
        "title": "TCGA Glioblastoma Multiforme (TCGA-GBM)",
        "organism": "Homo sapiens",
        "data_types": ["bulk RNA-seq", "WES/WGS", "methylation array", "microarray"],
        "sample_count": 617,
        "recurrent_sample_count": 13,
        "tumor_subtypes": ["GBM"],
        "molecular_markers": ["IDH1", "IDH2", "MGMT", "TERT", "ATRX", "TP53", "EGFR", "PTEN"],
        "treatment_info": "Variable; see GDC portal for case-level treatment data",
        "summary": (
            "The Cancer Genome Atlas Glioblastoma Multiforme project includes multi-omics "
            "profiling of GBM tumors. Contains a subset of recurrent tumor samples with "
            "whole-exome sequencing, RNA-seq, methylation array, and copy number data."
        ),
        "contributors": "The Cancer Genome Atlas Research Network",
        "institution": "NCI / NHGRI",
        "country": "USA",
        "publication_date": "2008-01-01",
        "pubmed_ids": ["23629348", "26061751"],
        "source_url": "https://portal.gdc.cancer.gov/projects/TCGA-GBM",
    },
    {
        "id": "TCGA_TCGA-LGG",
        "source": "TCGA",
        "accession": "TCGA-LGG",
        "title": "TCGA Low Grade Glioma (TCGA-LGG)",
        "organism": "Homo sapiens",
        "data_types": ["bulk RNA-seq", "WES/WGS", "methylation array", "microarray"],
        "sample_count": 516,
        "recurrent_sample_count": 0,
        "tumor_subtypes": ["Astrocytoma", "Oligodendroglioma", "Oligoastrocytoma"],
        "molecular_markers": ["IDH1", "IDH2", "MGMT", "1p/19q", "ATRX", "TP53", "CIC", "FUBP1"],
        "treatment_info": "Variable; see GDC portal for case-level treatment data",
        "summary": (
            "The Cancer Genome Atlas Low Grade Glioma project includes comprehensive "
            "molecular profiling of WHO grade II-III diffuse gliomas."
        ),
        "contributors": "The Cancer Genome Atlas Research Network",
        "institution": "NCI / NHGRI",
        "country": "USA",
        "publication_date": "2008-01-01",
        "pubmed_ids": ["26061373"],
        "source_url": "https://portal.gdc.cancer.gov/projects/TCGA-LGG",
    },
]


def fetch_tcga_datasets(**kwargs):
    """Fetch TCGA glioma project metadata from the GDC API.

    Falls back to curated metadata if the API is unavailable.

    Returns:
        List of dataset dicts in unified schema.
    """
    datasets = []

    for project_id in TCGA_PROJECTS:
        project_data = _query_gdc_project(project_id)
        if not project_data:
            continue

        recurrent_count = _count_recurrent_cases(project_id)
        entry = _build_tcga_entry(project_id, project_data, recurrent_count)
        datasets.append(entry)
        logger.info("Fetched TCGA project: %s (%d cases)", project_id, entry["sample_count"])

    if datasets:
        return datasets

    # Fallback to curated metadata
    logger.info("Using curated TCGA metadata (%d entries)", len(TCGA_FALLBACK))
    return [make_dataset_entry(**entry) for entry in TCGA_FALLBACK]
