#!/usr/bin/env python3
"""
cBioPortal data source fetcher for recurrent glioma studies.

Uses the cBioPortal REST API to search for glioma/GBM studies and checks
whether they contain recurrent samples via sample-level metadata.
"""

import logging
import time

import requests

from scripts.utils import is_recurrent_glioma, make_dataset_entry

logger = logging.getLogger(__name__)

CBIOPORTAL_API = "https://www.cbioportal.org/api"
HTTP_SESSION = requests.Session()
HTTP_SESSION.headers.update({
    "User-Agent": "RecurrentGliomaExplorer/1.0",
    "Accept": "application/json",
})

# Rate limiting for cBioPortal
_RATE_LIMIT_DELAY = 0.5

GLIOMA_KEYWORDS = [
    "glioma", "glioblastoma", "gbm", "astrocytoma",
    "oligodendroglioma", "brain", "gliom",
]

# Studies known to have recurrent glioma samples (fallback)
KNOWN_RECURRENT_STUDIES = {
    "lgg_ucsf_2014",
    "gbm_tcga",
    "lgg_tcga",
    "gbm_cptac_2021",
    "glass_dfci_2019",
    "gbm_columbia_2019",
    "gbm_mskcc_2019",
}


def _fetch_all_studies():
    """Fetch the full study list from cBioPortal."""
    try:
        resp = HTTP_SESSION.get(f"{CBIOPORTAL_API}/studies", timeout=30)
        if resp.status_code != 200:
            logger.warning("cBioPortal studies endpoint returned status %d", resp.status_code)
            return []
        return resp.json()
    except Exception as exc:
        logger.warning("Failed to fetch cBioPortal studies: %s", exc)
        return []


def _is_glioma_study(study):
    """Check if a study is glioma-related based on name and description."""
    text = f"{study.get('name', '')} {study.get('description', '')}".lower()
    return any(kw in text for kw in GLIOMA_KEYWORDS)


def _check_recurrent_samples(study_id):
    """Check if a study has recurrent samples by querying sample-level data.

    Returns (has_recurrent, recurrent_count, total_count).
    """
    try:
        resp = HTTP_SESSION.get(
            f"{CBIOPORTAL_API}/studies/{study_id}/samples",
            timeout=20,
        )
        if resp.status_code != 200:
            return False, None, None

        samples = resp.json()
        total = len(samples)

        recurrent_keywords = ["recur", "relaps", "progress", "second", "r_"]
        recurrent_count = 0
        for sample in samples:
            sample_id = sample.get("sampleId", "").lower()
            sample_type = sample.get("sampleType", "").lower()
            combined = f"{sample_id} {sample_type}"
            if any(kw in combined for kw in recurrent_keywords):
                recurrent_count += 1

        return recurrent_count > 0, recurrent_count, total

    except Exception as exc:
        logger.debug("Failed to check samples for %s: %s", study_id, exc)
        return False, None, None


def _fetch_molecular_profiles(study_id):
    """Fetch molecular profile types for a study."""
    try:
        resp = HTTP_SESSION.get(
            f"{CBIOPORTAL_API}/studies/{study_id}/molecular-profiles",
            timeout=15,
        )
        if resp.status_code != 200:
            return []

        profiles = resp.json()
        data_types = set()

        type_map = {
            "MUTATION_EXTENDED": "WES/WGS",
            "COPY_NUMBER_ALTERATION": "WES/WGS",
            "MRNA_EXPRESSION": "bulk RNA-seq",
            "METHYLATION": "methylation array",
            "PROTEIN_LEVEL": "proteomics",
            "STRUCTURAL_VARIANT": "WES/WGS",
        }

        for profile in profiles:
            mol_type = profile.get("molecularAlterationType", "")
            mapped = type_map.get(mol_type)
            if mapped:
                data_types.add(mapped)

        return sorted(data_types)

    except Exception as exc:
        logger.debug("Failed to fetch profiles for %s: %s", study_id, exc)
        return []


def _infer_subtypes(study):
    """Infer tumor subtypes from study metadata."""
    text = f"{study.get('name', '')} {study.get('description', '')}".lower()
    subtypes = []
    if any(t in text for t in ["glioblastoma", "gbm"]):
        subtypes.append("GBM")
    if "astrocytoma" in text:
        subtypes.append("Astrocytoma")
    if "oligodendroglioma" in text:
        subtypes.append("Oligodendroglioma")
    if "low grade glioma" in text or "lgg" in text:
        subtypes.extend(["Astrocytoma", "Oligodendroglioma"])
    if not subtypes and "glioma" in text:
        subtypes.append("Glioma")
    return sorted(set(subtypes))


def fetch_cbio_datasets(existing_ids=None, **kwargs):
    """Fetch recurrent glioma studies from cBioPortal.

    Queries the full study list, filters for glioma studies, then checks
    each one for recurrent samples.

    Args:
        existing_ids: Set of dataset IDs to skip.

    Returns:
        List of dataset dicts in unified schema.
    """
    existing_ids = existing_ids or set()
    studies = _fetch_all_studies()
    if not studies:
        logger.warning("No studies fetched from cBioPortal")
        return []

    glioma_studies = [s for s in studies if _is_glioma_study(s)]
    logger.info(
        "Found %d glioma-related studies out of %d total on cBioPortal",
        len(glioma_studies),
        len(studies),
    )

    datasets = []
    for study in glioma_studies:
        study_id = study.get("studyId", "")
        ds_id = f"cBioPortal_{study_id}"

        if ds_id in existing_ids:
            continue

        name = study.get("name", "")
        description = study.get("description", "")

        # Check if study name/description mentions recurrence
        text_relevant = is_recurrent_glioma(name, description)

        # Check sample-level data for recurrent samples
        has_recurrent, recurrent_count, total_count = False, None, None
        if text_relevant or study_id in KNOWN_RECURRENT_STUDIES:
            has_recurrent, recurrent_count, total_count = _check_recurrent_samples(study_id)
            time.sleep(_RATE_LIMIT_DELAY)

        if not text_relevant and not has_recurrent and study_id not in KNOWN_RECURRENT_STUDIES:
            continue

        # Fetch molecular profiles
        data_types = _fetch_molecular_profiles(study_id)
        time.sleep(_RATE_LIMIT_DELAY)

        sample_count = total_count or study.get("allSampleCount", 0)

        ds = make_dataset_entry(
            id=ds_id,
            source="cBioPortal",
            accession=study_id,
            title=name,
            organism="Homo sapiens",
            data_types=data_types or ["WES/WGS"],
            sample_count=sample_count,
            recurrent_sample_count=recurrent_count,
            tumor_subtypes=_infer_subtypes(study),
            summary=description,
            publication_date=study.get("importDate", ""),
            pubmed_ids=[str(study["pmid"])] if study.get("pmid") else [],
            source_url=f"https://www.cbioportal.org/study/summary?id={study_id}",
        )
        datasets.append(ds)
        logger.info(
            "  Added cBioPortal study: %s (%d samples, %s recurrent)",
            study_id,
            sample_count,
            recurrent_count if recurrent_count is not None else "unknown",
        )

    logger.info("cBioPortal fetch complete: %d studies with recurrent glioma data", len(datasets))
    return datasets
