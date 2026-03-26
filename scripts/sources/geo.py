#!/usr/bin/env python3
"""
GEO data source fetcher for recurrent glioma datasets.

Uses the NCBI Entrez API (esearch + esummary) and fetches SOFT format
for detailed metadata (overall design, contributors, country, etc.).
Supports incremental updates via a configurable lookback window.
"""

import logging
import os
import re
import time
from datetime import datetime, timedelta

import requests
from Bio import Entrez

from scripts.utils import (
    classify_data_types,
    is_recurrent_glioma,
    make_dataset_entry,
    normalize_organism,
)

logger = logging.getLogger(__name__)

NCBI_EMAIL = os.environ.get("NCBI_EMAIL", "")
NCBI_API_KEY = os.environ.get("NCBI_API_KEY", "")

HTTP_SESSION = requests.Session()
HTTP_SESSION.headers.update({"User-Agent": "RecurrentGliomaExplorer/1.0"})

# Rate limiting: NCBI allows 3 req/s without API key, 10 req/s with key
_RATE_LIMIT_DELAY = 0.12 if NCBI_API_KEY else 0.35

# ---------------------------------------------------------------------------
# Search queries targeting recurrent glioma
# ---------------------------------------------------------------------------

RECURRENT_KEYWORDS = [
    "recurrent glioma",
    "recurrent glioblastoma",
    "recurrent GBM",
    "recurrent astrocytoma",
    "recurrent oligodendroglioma",
    "relapsed glioma",
    "relapsed glioblastoma",
    "progressive glioblastoma",
    "progressive glioma",
    "glioma recurrence",
    "glioblastoma recurrence",
    "glioma progression",
    "glioma evolution",
    "glioblastoma evolution",
    "tumor evolution glioma",
    "longitudinal glioma",
    "longitudinal glioblastoma",
    "paired primary recurrent glioma",
    "matched primary recurrent glioma",
    "initial recurrent glioblastoma",
    "second surgery glioma",
    "reoperation glioblastoma",
    "post-treatment glioblastoma",
    "treatment resistant glioblastoma",
    "acquired resistance glioblastoma",
    "hypermutation glioma",
    "malignant transformation glioma",
    "transformed glioma",
]

ORGANISMS = ["Homo sapiens"]

GEO_DATA_TYPES = [
    "Expression profiling by high throughput sequencing",
    "Expression profiling by array",
    "Methylation profiling by array",
    "Methylation profiling by high throughput sequencing",
    "Genome binding/occupancy profiling by high throughput sequencing",
    "Genome variation profiling by high throughput sequencing",
    "Non-coding RNA profiling by high throughput sequencing",
]


def _setup_entrez():
    """Configure Entrez with email and optional API key."""
    Entrez.email = NCBI_EMAIL
    if NCBI_API_KEY:
        Entrez.api_key = NCBI_API_KEY


def _build_query():
    """Build the GEO search query string."""
    kw_part = " OR ".join(f'"{kw}"' for kw in RECURRENT_KEYWORDS)
    org_part = " OR ".join(f'"{org}"[Organism]' for org in ORGANISMS)
    type_part = " OR ".join(f'"{dt}"[DataSet Type]' for dt in GEO_DATA_TYPES)
    return f"({kw_part}) AND ({org_part}) AND ({type_part})"


def _clean_pubmed_ids(pubmed_list):
    """Extract numeric PubMed IDs from Entrez results."""
    if not pubmed_list:
        return []
    raw = "; ".join(str(item) for item in pubmed_list)
    numbers = re.findall(r"IntegerElement\((\d+)", raw)
    if not numbers:
        numbers = re.findall(r"\d+", raw)
    return numbers


def _batched(items, size):
    """Yield successive batches of the given size."""
    for start in range(0, len(items), size):
        yield items[start : start + size]


def _search_geo(full_refresh=False, recent_days=30, max_retries=3):
    """Run an esearch against GEO and return a list of GDS IDs."""
    query = _build_query()
    search_params = {
        "db": "gds",
        "term": query,
        "retmax": 10000,
        "usehistory": "y",
    }

    if not full_refresh:
        end_date = datetime.now().strftime("%Y/%m/%d")
        start_date = (datetime.now() - timedelta(days=recent_days)).strftime("%Y/%m/%d")
        search_params.update({
            "mindate": start_date,
            "maxdate": end_date,
            "datetype": "pdat",
        })
        logger.info("Incremental search: %s to %s", start_date, end_date)
    else:
        logger.info("Full refresh: no date restriction")

    logger.info("Search query (truncated): %s...", query[:150])

    for attempt in range(max_retries):
        try:
            handle = Entrez.esearch(**search_params)
            results = Entrez.read(handle)
            handle.close()
            id_list = results.get("IdList", [])
            logger.info("esearch returned %d IDs", len(id_list))
            return id_list
        except Exception as exc:
            logger.warning("esearch attempt %d/%d failed: %s", attempt + 1, max_retries, exc)
            if attempt < max_retries - 1:
                time.sleep(10)
    return []


def _fetch_summaries(id_list, max_retries=3, batch_size=200):
    """Fetch esummary records for a list of GDS IDs."""
    if not id_list:
        return []

    all_records = []
    for batch in _batched(id_list, batch_size):
        for attempt in range(max_retries):
            try:
                handle = Entrez.esummary(db="gds", id=",".join(batch))
                records = Entrez.read(handle)
                handle.close()
                all_records.extend(records)
                logger.info("Fetched summaries: %d / %d", len(all_records), len(id_list))
                break
            except Exception as exc:
                logger.warning(
                    "esummary attempt %d/%d failed: %s", attempt + 1, max_retries, exc
                )
                if attempt < max_retries - 1:
                    time.sleep(10)
                else:
                    logger.error("Skipping batch of %d IDs", len(batch))
        time.sleep(_RATE_LIMIT_DELAY)

    return all_records


def _fetch_soft(accession):
    """Fetch SOFT-format metadata for a GSE accession."""
    url = (
        f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={accession}"
        "&targ=self&form=text&view=full"
    )
    try:
        resp = HTTP_SESSION.get(url, timeout=20)
        if resp.status_code != 200:
            logger.warning("SOFT fetch for %s returned status %d", accession, resp.status_code)
            return {}

        info = {
            "overall_design": "",
            "contributors": [],
            "lab": "",
            "institute": "",
            "country": "",
            "series_type": [],
        }

        for raw_line in resp.text.split("\n"):
            line = raw_line.strip()
            if line.startswith("!Series_overall_design"):
                info["overall_design"] = line.split("=", 1)[1].strip()
            elif line.startswith("!Series_type"):
                val = line.split("=", 1)[1].strip()
                if val and val not in info["series_type"]:
                    info["series_type"].append(val)
            elif line.startswith("!Series_contributor"):
                contributor = line.split("=", 1)[1].strip()
                parts = [p.strip() for p in contributor.split(",") if p.strip()]
                if len(parts) >= 2:
                    formatted = f"{parts[-1]} {parts[0]}".strip()
                    if formatted and formatted not in info["contributors"]:
                        info["contributors"].append(formatted)
            elif line.startswith("!Series_contact_laboratory"):
                info["lab"] = line.split("=", 1)[1].strip()
            elif line.startswith("!Series_contact_institute"):
                info["institute"] = line.split("=", 1)[1].strip()
            elif line.startswith("!Series_contact_country"):
                info["country"] = line.split("=", 1)[1].strip()

        return info

    except Exception as exc:
        logger.warning("Failed to fetch SOFT for %s: %s", accession, exc)
        return {}


def _parse_record(record):
    """Parse a single GEO esummary record into the unified schema."""
    accession = record.get("Accession", "")
    if not accession.startswith("GSE"):
        return None

    title = record.get("title", "")
    summary = record.get("summary", "")

    # Only keep datasets related to recurrent glioma
    if not is_recurrent_glioma(title, summary):
        return None

    # Fetch SOFT for extra metadata
    soft = _fetch_soft(accession)
    time.sleep(_RATE_LIMIT_DELAY)

    overall_design = soft.get("overall_design", "")
    geo_data_type = "; ".join(soft.get("series_type", []))

    data_types = classify_data_types(title, summary, overall_design, geo_data_type)
    if not data_types:
        # Try to default to bulk RNA-seq if we have expression data
        if "expression profiling" in geo_data_type.lower():
            data_types = ["bulk RNA-seq"]
        else:
            data_types = ["unknown"]

    pubmed_ids = _clean_pubmed_ids(record.get("PubMedIds", []))

    return make_dataset_entry(
        id=f"GEO_{accession}",
        source="GEO",
        accession=accession,
        title=title,
        organism=normalize_organism(record.get("taxon", "")),
        data_types=data_types,
        sample_count=record.get("n_samples", 0),
        recurrent_sample_count=None,
        tumor_subtypes=_infer_tumor_subtypes(title, summary),
        summary=summary,
        contributors="; ".join(soft.get("contributors", [])),
        institution=soft.get("institute", ""),
        country=soft.get("country", ""),
        publication_date=record.get("PDAT", ""),
        pubmed_ids=pubmed_ids,
        source_url=f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={accession}",
    )


def _infer_tumor_subtypes(title, summary):
    """Infer glioma subtypes from text."""
    combined = f"{title} {summary}".lower()
    subtypes = []
    if any(t in combined for t in ["glioblastoma", "gbm"]):
        subtypes.append("GBM")
    if "astrocytoma" in combined:
        subtypes.append("Astrocytoma")
    if "oligodendroglioma" in combined:
        subtypes.append("Oligodendroglioma")
    if not subtypes and "glioma" in combined:
        subtypes.append("Glioma")
    return subtypes


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def fetch_geo_datasets(full_refresh=False, recent_days=30, existing_ids=None):
    """Fetch recurrent glioma datasets from GEO.

    Args:
        full_refresh: If True, search all of GEO history.
        recent_days: Lookback window for incremental updates.
        existing_ids: Set of dataset IDs already known (for skipping).

    Returns:
        List of dataset dicts in unified schema.
    """
    if not NCBI_EMAIL:
        logger.error(
            "NCBI_EMAIL environment variable not set. "
            "Set it to your email address to use NCBI Entrez."
        )
        return []

    existing_ids = existing_ids or set()
    _setup_entrez()

    id_list = _search_geo(full_refresh=full_refresh, recent_days=recent_days)
    if not id_list:
        logger.info("No GEO IDs found")
        return []

    summaries = _fetch_summaries(id_list)
    logger.info("Retrieved %d summaries from GEO", len(summaries))

    datasets = []
    skipped_existing = 0
    skipped_irrelevant = 0

    for idx, record in enumerate(summaries, 1):
        accession = record.get("Accession", "")
        geo_id = f"GEO_{accession}"

        if geo_id in existing_ids:
            skipped_existing += 1
            continue

        if idx % 25 == 0:
            logger.info("Processing record %d / %d", idx, len(summaries))

        parsed = _parse_record(record)
        if parsed:
            datasets.append(parsed)
            logger.info("  Added: %s - %s", accession, parsed["title"][:80])
        else:
            skipped_irrelevant += 1

    logger.info(
        "GEO fetch complete: %d new datasets, %d skipped (existing), %d skipped (irrelevant)",
        len(datasets),
        skipped_existing,
        skipped_irrelevant,
    )
    return datasets
