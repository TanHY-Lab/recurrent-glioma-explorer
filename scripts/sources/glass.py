#!/usr/bin/env python3
"""
GLASS (Glioma Longitudinal AnalySiS) consortium data source fetcher.

Attempts to fetch study metadata from the cBioPortal API, with a fallback
to well-known curated metadata about the GLASS consortium.
"""

import logging

import requests

from scripts.utils import make_dataset_entry

logger = logging.getLogger(__name__)

CBIOPORTAL_API = "https://www.cbioportal.org/api"
HTTP_SESSION = requests.Session()
HTTP_SESSION.headers.update({
    "User-Agent": "RecurrentGliomaExplorer/1.0",
    "Accept": "application/json",
})

# ---------------------------------------------------------------------------
# Curated GLASS metadata (fallback if API is unavailable)
# ---------------------------------------------------------------------------

GLASS_CURATED = [
    {
        "id": "GLASS_CONSORTIUM",
        "source": "GLASS",
        "accession": "GLASS",
        "title": "GLASS Consortium - Glioma Longitudinal AnalySiS",
        "organism": "Homo sapiens",
        "data_types": ["WES", "WGS", "bulk RNA-seq", "methylation array"],
        "sample_count": 1147,
        "recurrent_sample_count": 554,
        "tumor_subtypes": ["GBM", "Astrocytoma", "Oligodendroglioma"],
        "molecular_markers": ["IDH1", "IDH2", "1p/19q", "MGMT", "TERT"],
        "treatment_info": "Pre- and post-treatment paired samples; TMZ, radiation, bevacizumab",
        "summary": (
            "The GLASS consortium is a large-scale collaborative effort to characterize "
            "the longitudinal genomic landscape of diffuse gliomas. The project collected "
            "whole-exome sequencing, whole-genome sequencing, RNA-seq, and DNA methylation "
            "data from matched initial and recurrent glioma specimens across multiple "
            "institutions worldwide. Key findings include characterization of treatment-"
            "associated hypermutation, tumor microenvironment evolution, and clonal dynamics "
            "during glioma progression."
        ),
        "contributors": "GLASS Consortium",
        "institution": "Multi-institutional consortium",
        "country": "International",
        "publication_date": "2019-02-13",
        "pubmed_ids": ["30753390", "35163337", "34297920"],
        "source_url": "https://www.synapse.org/#!Synapse:syn17038081",
    },
    {
        "id": "GLASS_cBioPortal",
        "source": "GLASS",
        "accession": "glass_dfci_2019",
        "title": "GLASS - Glioma Longitudinal AnalySiS (cBioPortal)",
        "organism": "Homo sapiens",
        "data_types": ["WES", "WGS"],
        "sample_count": 580,
        "recurrent_sample_count": 290,
        "tumor_subtypes": ["GBM", "Astrocytoma", "Oligodendroglioma"],
        "molecular_markers": ["IDH1", "IDH2", "1p/19q", "MGMT"],
        "treatment_info": "Paired initial and recurrent tumor samples",
        "summary": (
            "Longitudinal whole-exome/whole-genome sequencing of matched initial and "
            "recurrent diffuse gliomas from the GLASS consortium, available via cBioPortal."
        ),
        "contributors": "GLASS Consortium",
        "institution": "Multi-institutional consortium",
        "country": "International",
        "publication_date": "2019-02-13",
        "pubmed_ids": ["30753390"],
        "source_url": "https://www.cbioportal.org/study/summary?id=glass_dfci_2019",
    },
]


def _try_cbioportal_glass():
    """Attempt to fetch GLASS study info from cBioPortal API."""
    try:
        resp = HTTP_SESSION.get(
            f"{CBIOPORTAL_API}/studies",
            params={"keyword": "GLASS"},
            timeout=15,
        )
        if resp.status_code != 200:
            logger.warning("cBioPortal API returned status %d", resp.status_code)
            return []

        studies = resp.json()
        glass_studies = [s for s in studies if "glass" in s.get("studyId", "").lower()]

        datasets = []
        for study in glass_studies:
            study_id = study.get("studyId", "")
            ds = make_dataset_entry(
                id=f"GLASS_{study_id}",
                source="GLASS",
                accession=study_id,
                title=study.get("name", ""),
                organism="Homo sapiens",
                data_types=["WES", "WGS"],
                sample_count=study.get("allSampleCount", 0),
                tumor_subtypes=["GBM", "Astrocytoma", "Oligodendroglioma"],
                summary=study.get("description", ""),
                publication_date=study.get("importDate", ""),
                pubmed_ids=[str(study["pmid"])] if study.get("pmid") else [],
                source_url=f"https://www.cbioportal.org/study/summary?id={study_id}",
            )
            datasets.append(ds)

        return datasets

    except Exception as exc:
        logger.warning("cBioPortal API query failed: %s", exc)
        return []


def fetch_glass_datasets(**kwargs):
    """Fetch GLASS consortium datasets.

    Tries the cBioPortal API first. Falls back to curated metadata if the
    API is unavailable or returns no GLASS studies.

    Returns:
        List of dataset dicts in unified schema.
    """
    api_results = _try_cbioportal_glass()

    if api_results:
        logger.info("Fetched %d GLASS studies from cBioPortal API", len(api_results))
        # Merge with the main curated Synapse entry
        api_ids = {ds["id"] for ds in api_results}
        for curated in GLASS_CURATED:
            if curated["id"] not in api_ids:
                ds = make_dataset_entry(**curated)
                api_results.append(ds)
        return api_results

    logger.info("Using curated GLASS metadata (%d entries)", len(GLASS_CURATED))
    return [make_dataset_entry(**entry) for entry in GLASS_CURATED]
