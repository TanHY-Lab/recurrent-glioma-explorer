#!/usr/bin/env python3
"""
Other curated data sources for recurrent glioma research.

Provides hardcoded metadata entries for well-known datasets that lack
a convenient programmatic API, including Ivy GAP, REMBRANDT, G-SAM/EORTC,
GBM CARE, CELLO2/CGGA-AGGA, OpenPBTA/CBTN, MSK-IMPACT, and AACR GENIE.
"""

import logging

from scripts.utils import make_dataset_entry

logger = logging.getLogger(__name__)

OTHER_DATASETS = [
    # -----------------------------------------------------------------------
    # Ivy Glioblastoma Atlas Project (Ivy GAP)
    # -----------------------------------------------------------------------
    {
        "id": "IvyGAP",
        "source": "IvyGAP",
        "accession": "IvyGAP",
        "title": "Ivy Glioblastoma Atlas Project (Ivy GAP)",
        "organism": "Homo sapiens",
        "data_types": ["bulk RNA-seq", "spatial transcriptomics"],
        "sample_count": 270,
        "recurrent_sample_count": 12,
        "tumor_subtypes": ["GBM"],
        "molecular_markers": ["IDH1", "EGFR", "PTEN", "TP53"],
        "treatment_info": (
            "Anatomic transcriptomic atlas of GBM; includes some recurrent "
            "tumor specimens with treatment history"
        ),
        "summary": (
            "The Ivy Glioblastoma Atlas Project provides in situ hybridization (ISH) "
            "and laser-microdissection-based transcriptomic data from anatomic structures "
            "within glioblastoma tumors. 270 RNA-seq samples from 42 tumors capturing "
            "distinct histological features: leading edge, infiltrating tumor, cellular "
            "tumor, perinecrotic zone, and pseudopalisading cells around necrosis. "
            "Includes paired laser-capture microdissected and bulk tumor samples."
        ),
        "contributors": "Allen Institute for Brain Science; Ben Barres Lab",
        "institution": "Allen Institute for Brain Science",
        "country": "USA",
        "publication_date": "2017-11-01",
        "pubmed_ids": ["29084289"],
        "source_url": "https://glioblastoma.alleninstitute.org/",
    },
    # -----------------------------------------------------------------------
    # REMBRANDT
    # -----------------------------------------------------------------------
    {
        "id": "REMBRANDT",
        "source": "REMBRANDT",
        "accession": "GSE108476",
        "title": "REMBRANDT - Repository for Molecular BRAin Neoplasia DaTa",
        "organism": "Homo sapiens",
        "data_types": ["microarray", "WES/WGS"],
        "sample_count": 671,
        "recurrent_sample_count": 35,
        "tumor_subtypes": ["GBM", "Astrocytoma", "Oligodendroglioma"],
        "molecular_markers": ["IDH1", "EGFR", "PTEN", "TP53", "MGMT"],
        "treatment_info": "Multi-institutional clinical trial cohort with treatment annotations",
        "summary": (
            "REMBRANDT (REpository for Molecular BRAin Neoplasia DaTa) is a multi-"
            "institutional clinical genomics dataset comprising gene expression microarray "
            "and copy number data from 671 brain tumor specimens, including glioblastoma, "
            "astrocytoma, and oligodendroglioma. Contains a subset of recurrent glioma "
            "samples with clinical outcome data. Originally curated by NCI and now "
            "available through GEO (GSE108476)."
        ),
        "contributors": "NCI REMBRANDT Project",
        "institution": "National Cancer Institute",
        "country": "USA",
        "publication_date": "2018-01-15",
        "pubmed_ids": ["15827123"],
        "source_url": "https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE108476",
    },
    # -----------------------------------------------------------------------
    # G-SAM / EORTC
    # -----------------------------------------------------------------------
    {
        "id": "GSAM_EORTC",
        "source": "G-SAM/EORTC",
        "accession": "EGAS00001004582",
        "title": "G-SAM / EORTC 26091 - Glioblastoma Spatial and Molecular Analysis",
        "organism": "Homo sapiens",
        "data_types": ["WES/WGS", "bulk RNA-seq"],
        "sample_count": 222,
        "recurrent_sample_count": 110,
        "tumor_subtypes": ["GBM"],
        "molecular_markers": ["IDH1", "MGMT", "TERT", "EGFR"],
        "treatment_info": (
            "Prospective EORTC trial with matched primary and recurrent GBM samples; "
            "standard-of-care TMZ + radiation"
        ),
        "summary": (
            "The Glioblastoma Spatial and Molecular (G-SAM) study conducted under the "
            "EORTC 26091 clinical trial provides multi-region whole-genome and "
            "transcriptomic sequencing of matched primary and recurrent glioblastoma. "
            "Examines spatial heterogeneity, clonal evolution, and treatment-induced "
            "genomic changes. Data hosted on the European Genome-phenome Archive (EGA)."
        ),
        "contributors": "Erasmus MC; EORTC Brain Tumour Group",
        "institution": "Erasmus University Medical Center",
        "country": "Netherlands",
        "publication_date": "2022-09-01",
        "pubmed_ids": ["36055464"],
        "source_url": "https://ega-archive.org/studies/EGAS00001004582",
    },
    # -----------------------------------------------------------------------
    # GBM CARE Consortium
    # -----------------------------------------------------------------------
    {
        "id": "GBM_CARE",
        "source": "GBM CARE",
        "accession": "GBM_CARE",
        "title": "GBM CARE Consortium - Comprehensive Analysis of Recurrent GBM Evolution",
        "organism": "Homo sapiens",
        "data_types": ["WES/WGS", "bulk RNA-seq", "methylation array"],
        "sample_count": 304,
        "recurrent_sample_count": 152,
        "tumor_subtypes": ["GBM"],
        "molecular_markers": ["IDH1", "MGMT", "TERT", "EGFR", "PTEN", "NF1"],
        "treatment_info": (
            "Paired primary-recurrent GBM from multiple European centers; "
            "TMZ-based chemotherapy and radiotherapy"
        ),
        "summary": (
            "The GBM CARE (Comprehensive Analysis of Recurrent Evolution) consortium "
            "collected matched primary and recurrent GBM specimens from multiple "
            "European neuro-oncology centers. Multi-omics profiling (WES, RNA-seq, "
            "DNA methylation) was performed to characterize genomic and epigenomic "
            "evolution during GBM recurrence, identifying recurrence-specific driver "
            "events and treatment-associated mutational patterns."
        ),
        "contributors": "GBM CARE Consortium",
        "institution": "German Cancer Research Center (DKFZ)",
        "country": "Germany",
        "publication_date": "2023-03-15",
        "pubmed_ids": [],
        "source_url": "",
    },
    # -----------------------------------------------------------------------
    # CELLO2 / CGGA-AGGA
    # -----------------------------------------------------------------------
    {
        "id": "CELLO2_CGGA_AGGA",
        "source": "CELLO2/CGGA-AGGA",
        "accession": "CELLO2",
        "title": "CELLO2 / CGGA-AGGA - Chinese/Asian Glioma Genome Atlas Expansion",
        "organism": "Homo sapiens",
        "data_types": ["bulk RNA-seq", "WES/WGS", "methylation array"],
        "sample_count": 2000,
        "recurrent_sample_count": 500,
        "tumor_subtypes": ["GBM", "Astrocytoma", "Oligodendroglioma"],
        "molecular_markers": ["IDH1", "IDH2", "1p/19q", "MGMT", "TERT", "ATRX"],
        "treatment_info": (
            "Large-scale Chinese and Asian glioma cohort with primary and recurrent samples; "
            "includes treatment response annotations"
        ),
        "summary": (
            "CELLO2 (CancEr celluLar LOngitudinal) and the expanded CGGA-AGGA (Asian "
            "Glioma Genome Atlas) provide a comprehensive multi-omics resource for "
            "approximately 2,000 glioma specimens from Chinese and Asian populations. "
            "Includes matched primary-recurrent pairs with genomic, transcriptomic, and "
            "epigenomic profiling, enabling analysis of recurrence-associated molecular "
            "changes in Asian glioma patients."
        ),
        "contributors": "CGGA Consortium; Beijing Tiantan Hospital",
        "institution": "Beijing Tiantan Hospital / Capital Medical University",
        "country": "China",
        "publication_date": "2023-06-01",
        "pubmed_ids": ["37264039"],
        "source_url": "http://www.cgga.org.cn/",
    },
    # -----------------------------------------------------------------------
    # OpenPBTA / CBTN
    # -----------------------------------------------------------------------
    {
        "id": "OpenPBTA_CBTN",
        "source": "OpenPBTA/CBTN",
        "accession": "OpenPBTA",
        "title": "Open Pediatric Brain Tumor Atlas (OpenPBTA) / CBTN",
        "organism": "Homo sapiens",
        "data_types": ["WES/WGS", "bulk RNA-seq", "scRNA-seq"],
        "sample_count": 1074,
        "recurrent_sample_count": 130,
        "tumor_subtypes": ["GBM", "Astrocytoma", "Oligodendroglioma"],
        "molecular_markers": ["H3K27M", "H3G34R/V", "BRAF", "IDH1", "TP53", "ATRX"],
        "treatment_info": (
            "Pediatric brain tumors with some adult recurrent glioma; "
            "treatment annotations available in clinical data"
        ),
        "summary": (
            "The Open Pediatric Brain Tumor Atlas (OpenPBTA), a project of the "
            "Children's Brain Tumor Network (CBTN), provides harmonized multi-omics "
            "data for over 1,000 pediatric and young adult brain tumor samples. "
            "Includes whole-genome sequencing, RNA-seq, and single-cell data with "
            "a subset of recurrent/progressive glioma specimens. Data and analyses "
            "are openly available on the CAVATICA platform."
        ),
        "contributors": "Children's Brain Tumor Network (CBTN); Alex's Lemonade Stand Foundation",
        "institution": "Children's Hospital of Philadelphia",
        "country": "USA",
        "publication_date": "2023-02-01",
        "pubmed_ids": ["36747053"],
        "source_url": "https://github.com/PediatricOpenTargets/OpenPBTA-analysis",
    },
    # -----------------------------------------------------------------------
    # MSK-IMPACT
    # -----------------------------------------------------------------------
    {
        "id": "MSK_IMPACT_Glioma",
        "source": "MSK-IMPACT",
        "accession": "MSK-IMPACT",
        "title": "MSK-IMPACT Targeted Panel Sequencing - Glioma Cohort",
        "organism": "Homo sapiens",
        "data_types": ["WES/WGS"],
        "sample_count": 2500,
        "recurrent_sample_count": 800,
        "tumor_subtypes": ["GBM", "Astrocytoma", "Oligodendroglioma"],
        "molecular_markers": [
            "IDH1", "IDH2", "TP53", "ATRX", "TERT", "EGFR",
            "PTEN", "NF1", "PIK3CA", "PDGFRA",
        ],
        "treatment_info": (
            "Clinical targeted sequencing with extensive treatment and outcome annotations; "
            "many recurrent samples from clinical care"
        ),
        "summary": (
            "MSK-IMPACT is a FDA-authorized targeted sequencing panel covering 468+ "
            "cancer-associated genes, applied to clinical care at Memorial Sloan Kettering. "
            "The glioma cohort includes approximately 2,500 tumor samples with a "
            "substantial fraction of recurrent gliomas sequenced as part of clinical care. "
            "Somatic mutations, copy number alterations, and structural variants are "
            "available through cBioPortal."
        ),
        "contributors": "Memorial Sloan Kettering Cancer Center",
        "institution": "Memorial Sloan Kettering Cancer Center",
        "country": "USA",
        "publication_date": "2017-05-01",
        "pubmed_ids": ["28481359"],
        "source_url": "https://www.cbioportal.org/study/summary?id=msk_impact_2017",
    },
    # -----------------------------------------------------------------------
    # AACR GENIE
    # -----------------------------------------------------------------------
    {
        "id": "AACR_GENIE_Glioma",
        "source": "AACR GENIE",
        "accession": "GENIE",
        "title": "AACR Project GENIE - Glioma/GBM Subset",
        "organism": "Homo sapiens",
        "data_types": ["WES/WGS"],
        "sample_count": 5000,
        "recurrent_sample_count": 1500,
        "tumor_subtypes": ["GBM", "Astrocytoma", "Oligodendroglioma"],
        "molecular_markers": [
            "IDH1", "IDH2", "TP53", "ATRX", "TERT", "EGFR",
            "PTEN", "NF1", "PIK3CA", "CDKN2A",
        ],
        "treatment_info": (
            "Multi-institutional clinical sequencing data with treatment and "
            "outcome annotations for a subset of patients"
        ),
        "summary": (
            "AACR Project GENIE (Genomics Evidence Neoplasia Information Exchange) "
            "aggregates clinical-grade genomic data from multiple cancer centers worldwide. "
            "The glioma/GBM subset includes approximately 5,000 tumor samples from panels "
            "including MSK-IMPACT, DFCI OncoPanel, VICC, and others. A significant fraction "
            "represents recurrent gliomas sequenced during clinical care. Data are released "
            "publicly in periodic releases through Synapse."
        ),
        "contributors": "AACR Project GENIE Consortium",
        "institution": "American Association for Cancer Research",
        "country": "International",
        "publication_date": "2017-10-01",
        "pubmed_ids": ["28572459"],
        "source_url": "https://www.synapse.org/#!Synapse:syn7222066",
    },

    # -----------------------------------------------------------------------
    # Renji Hospital — Mouse Recurrent Glioma Model (Tan & Bao Lab)
    # -----------------------------------------------------------------------
    {
        "id": "Renji_RGM",
        "source": "Renji Hospital",
        "accession": "Renji-RGM-2026",
        "title": (
            "Single-cell and Spatial Transcriptomic Atlas of Mouse "
            "Recurrent Glioma Model"
        ),
        "organism": "Mus musculus",
        "data_types": ["scRNA-seq", "spatial transcriptomics"],
        "sample_count": None,
        "recurrent_sample_count": None,
        "tumor_subtypes": ["Glioma"],
        "molecular_markers": [],
        "treatment_info": "",
        "summary": (
            "Single-cell RNA sequencing (scRNA-seq) and spatial transcriptomics profiling "
            "of a mouse recurrent glioma model constructed at the Department of Neurosurgery, "
            "Renji Hospital, Shanghai Jiao Tong University School of Medicine. This dataset "
            "characterizes the tumor microenvironment evolution during glioma recurrence at "
            "single-cell and spatial resolution. Data pending publication — will be publicly "
            "available upon manuscript acceptance."
        ),
        "contributors": "Tan Haoyuan*, ..., Zhao Dongxu#, Bao Yinghui#",
        "institution": (
            "Department of Neurosurgery, Renji Hospital, "
            "Shanghai Jiao Tong University School of Medicine; "
            "School of Life Sciences, Fudan University; "
            "Naval Medical University"
        ),
        "country": "China",
        "publication_date": "",
        "pubmed_ids": [],
        "source_url": "",
    },
]


def fetch_other_datasets(**kwargs):
    """Return curated metadata for other well-known recurrent glioma datasets.

    Returns:
        List of dataset dicts in unified schema.
    """
    logger.info("Loading %d curated other-source datasets", len(OTHER_DATASETS))
    return [make_dataset_entry(**entry) for entry in OTHER_DATASETS]
