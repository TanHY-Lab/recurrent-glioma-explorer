#!/usr/bin/env python3
"""
CPTAC-GBM data source fetcher.

Provides curated metadata for the CPTAC Glioblastoma proteogenomic study,
which includes 228 tumor samples from 200 patients with 28 matched recurrent
specimens profiled across 14 omics platforms.
"""

import logging

from scripts.utils import make_dataset_entry

logger = logging.getLogger(__name__)

CPTAC_DATASETS = [
    {
        "id": "CPTAC_GBM",
        "source": "CPTAC",
        "accession": "CPTAC-GBM",
        "title": "CPTAC Glioblastoma Discovery Study - Proteogenomic Characterization",
        "organism": "Homo sapiens",
        "data_types": [
            "proteomics",
            "bulk RNA-seq",
            "WES/WGS",
            "methylation array",
            "scRNA-seq",
            "snRNA-seq",
            "spatial transcriptomics",
            "ATAC-seq",
        ],
        "sample_count": 228,
        "recurrent_sample_count": 28,
        "tumor_subtypes": ["GBM"],
        "molecular_markers": [
            "IDH1", "EGFR", "EGFRvIII", "PTEN", "TP53", "TERT",
            "NF1", "PDGFRA", "CDK4", "MDM2", "MGMT",
        ],
        "treatment_info": (
            "Includes 28 matched recurrent samples post standard-of-care treatment "
            "(TMZ + radiation). Proteogenomic analysis of treatment response and "
            "resistance mechanisms."
        ),
        "summary": (
            "The CPTAC Glioblastoma Discovery Study provides deep proteogenomic "
            "characterization of 228 tumor samples from 200 GBM patients, including "
            "28 matched recurrent tumors. Data were generated across 14 omics platforms "
            "including whole-exome sequencing, RNA-seq, global proteomics, "
            "phosphoproteomics, acetylproteomics, ubiquitylomics, single-cell RNA-seq, "
            "single-nucleus RNA-seq, spatial transcriptomics, ATAC-seq, DNA methylation "
            "arrays, lipidomics, metabolomics, and whole-genome sequencing. The study "
            "identified proteomic subtypes of GBM and characterized immune cell "
            "infiltration patterns, metabolic reprogramming, and signaling pathway "
            "alterations associated with tumor recurrence."
        ),
        "contributors": (
            "Clinical Proteomic Tumor Analysis Consortium (CPTAC); "
            "National Cancer Institute"
        ),
        "institution": "NCI / Clinical Proteomic Tumor Analysis Consortium",
        "country": "USA",
        "publication_date": "2021-02-18",
        "pubmed_ids": ["33577785"],
        "source_url": "https://proteomic.datacommons.cancer.gov/pdc/study/PDC000204",
    },
    {
        "id": "CPTAC_GBM_GDC",
        "source": "CPTAC",
        "accession": "CPTAC-GBM-GDC",
        "title": "CPTAC GBM Data on GDC (Genomic Data Commons)",
        "organism": "Homo sapiens",
        "data_types": ["WES/WGS", "bulk RNA-seq", "methylation array"],
        "sample_count": 228,
        "recurrent_sample_count": 28,
        "tumor_subtypes": ["GBM"],
        "molecular_markers": ["IDH1", "EGFR", "PTEN", "TP53", "TERT"],
        "treatment_info": "Matched primary and recurrent tumor pairs",
        "summary": (
            "Genomic and transcriptomic data from the CPTAC GBM study hosted on the "
            "NCI Genomic Data Commons portal. Includes whole-exome sequencing, RNA-seq, "
            "and methylation array data with clinical annotations."
        ),
        "contributors": "Clinical Proteomic Tumor Analysis Consortium (CPTAC)",
        "institution": "NCI / Genomic Data Commons",
        "country": "USA",
        "publication_date": "2021-02-18",
        "pubmed_ids": ["33577785"],
        "source_url": "https://portal.gdc.cancer.gov/projects/CPTAC-3",
    },
]


def fetch_cptac_datasets(**kwargs):
    """Return curated CPTAC-GBM dataset metadata.

    Returns:
        List of dataset dicts in unified schema.
    """
    logger.info("Loading %d curated CPTAC datasets", len(CPTAC_DATASETS))
    return [make_dataset_entry(**entry) for entry in CPTAC_DATASETS]
