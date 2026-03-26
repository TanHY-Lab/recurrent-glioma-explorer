#!/usr/bin/env python3
"""
CGGA (Chinese Glioma Genome Atlas) data source fetcher.

Provides curated metadata for the well-known CGGA dataset batches
including RNA-seq, WES, methylation, and miRNA datasets.
"""

import logging

from scripts.utils import make_dataset_entry

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Curated CGGA dataset metadata
# ---------------------------------------------------------------------------

CGGA_DATASETS = [
    {
        "id": "CGGA_RNAseq_Batch1",
        "source": "CGGA",
        "accession": "CGGA_RNAseq_325",
        "title": "CGGA RNA-seq Batch 1 (mRNAseq_325)",
        "organism": "Homo sapiens",
        "data_types": ["bulk RNA-seq"],
        "sample_count": 325,
        "recurrent_sample_count": 109,
        "tumor_subtypes": ["GBM", "Astrocytoma", "Oligodendroglioma"],
        "molecular_markers": ["IDH1", "IDH2", "1p/19q", "MGMT"],
        "treatment_info": "Primary and recurrent samples with treatment annotation",
        "summary": (
            "CGGA RNA-seq Batch 1 contains mRNA sequencing data for 325 glioma samples "
            "including primary and recurrent tumors across WHO grades II-IV. Includes "
            "IDH mutation status, 1p/19q codeletion status, and MGMT promoter methylation."
        ),
        "contributors": "Beijing Tiantan Hospital, Capital Medical University",
        "institution": "Beijing Tiantan Hospital",
        "country": "China",
        "publication_date": "2021-01-29",
        "pubmed_ids": ["33476548"],
        "source_url": "http://www.cgga.org.cn/download.jsp",
    },
    {
        "id": "CGGA_RNAseq_Batch2",
        "source": "CGGA",
        "accession": "CGGA_RNAseq_693",
        "title": "CGGA RNA-seq Batch 2 (mRNAseq_693)",
        "organism": "Homo sapiens",
        "data_types": ["bulk RNA-seq"],
        "sample_count": 693,
        "recurrent_sample_count": 188,
        "tumor_subtypes": ["GBM", "Astrocytoma", "Oligodendroglioma"],
        "molecular_markers": ["IDH1", "IDH2", "1p/19q", "MGMT"],
        "treatment_info": "Primary and recurrent samples with treatment annotation",
        "summary": (
            "CGGA RNA-seq Batch 2 contains mRNA sequencing data for 693 glioma samples "
            "including a significant proportion of recurrent cases. Provides gene expression "
            "profiles along with clinical and molecular annotations for Chinese glioma patients."
        ),
        "contributors": "Beijing Tiantan Hospital, Capital Medical University",
        "institution": "Beijing Tiantan Hospital",
        "country": "China",
        "publication_date": "2021-01-29",
        "pubmed_ids": ["33476548"],
        "source_url": "http://www.cgga.org.cn/download.jsp",
    },
    {
        "id": "CGGA_WES",
        "source": "CGGA",
        "accession": "CGGA_WES_286",
        "title": "CGGA Whole Exome Sequencing (286 samples)",
        "organism": "Homo sapiens",
        "data_types": ["WES/WGS"],
        "sample_count": 286,
        "recurrent_sample_count": 86,
        "tumor_subtypes": ["GBM", "Astrocytoma", "Oligodendroglioma"],
        "molecular_markers": ["IDH1", "IDH2", "TP53", "ATRX", "TERT"],
        "treatment_info": "Includes paired primary-recurrent samples",
        "summary": (
            "Whole exome sequencing of 286 Chinese glioma samples covering all WHO grades. "
            "Includes somatic mutation calls, copy number alterations, and mutational "
            "signature analyses. Contains paired primary and recurrent tumor specimens."
        ),
        "contributors": "Beijing Tiantan Hospital, Capital Medical University",
        "institution": "Beijing Tiantan Hospital",
        "country": "China",
        "publication_date": "2021-01-29",
        "pubmed_ids": ["33476548"],
        "source_url": "http://www.cgga.org.cn/download.jsp",
    },
    {
        "id": "CGGA_Methylation",
        "source": "CGGA",
        "accession": "CGGA_Methylation_159",
        "title": "CGGA DNA Methylation (159 samples)",
        "organism": "Homo sapiens",
        "data_types": ["methylation array"],
        "sample_count": 159,
        "recurrent_sample_count": 39,
        "tumor_subtypes": ["GBM", "Astrocytoma", "Oligodendroglioma"],
        "molecular_markers": ["MGMT", "IDH1", "IDH2"],
        "treatment_info": "Primary and recurrent glioma methylation profiles",
        "summary": (
            "DNA methylation profiling of 159 Chinese glioma samples using Illumina arrays. "
            "Provides genome-wide methylation data for classification and MGMT promoter "
            "methylation status assessment across glioma grades."
        ),
        "contributors": "Beijing Tiantan Hospital, Capital Medical University",
        "institution": "Beijing Tiantan Hospital",
        "country": "China",
        "publication_date": "2021-01-29",
        "pubmed_ids": ["33476548"],
        "source_url": "http://www.cgga.org.cn/download.jsp",
    },
    {
        "id": "CGGA_miRNA",
        "source": "CGGA",
        "accession": "CGGA_miRNA_198",
        "title": "CGGA miRNA Expression (198 samples)",
        "organism": "Homo sapiens",
        "data_types": ["microarray"],
        "sample_count": 198,
        "recurrent_sample_count": 53,
        "tumor_subtypes": ["GBM", "Astrocytoma", "Oligodendroglioma"],
        "molecular_markers": ["IDH1"],
        "treatment_info": "Primary and recurrent glioma samples",
        "summary": (
            "miRNA expression profiling of 198 Chinese glioma samples. Captures "
            "non-coding RNA expression changes across glioma grades and between "
            "primary and recurrent disease states."
        ),
        "contributors": "Beijing Tiantan Hospital, Capital Medical University",
        "institution": "Beijing Tiantan Hospital",
        "country": "China",
        "publication_date": "2021-01-29",
        "pubmed_ids": ["33476548"],
        "source_url": "http://www.cgga.org.cn/download.jsp",
    },
]


def fetch_cgga_datasets(**kwargs):
    """Return curated CGGA dataset metadata.

    Returns:
        List of dataset dicts in unified schema.
    """
    logger.info("Loading %d curated CGGA datasets", len(CGGA_DATASETS))
    return [make_dataset_entry(**entry) for entry in CGGA_DATASETS]
