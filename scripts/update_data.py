#!/usr/bin/env python3
"""
Recurrent Glioma Multi-Omics Explorer - Main Data Pipeline Orchestrator

Fetches recurrent glioma datasets from multiple sources (GEO, GLASS, CGGA,
TCGA, CPTAC, cBioPortal, and curated others), merges, deduplicates, validates,
and writes the result to data/datasets.json.

Usage:
    python scripts/update_data.py                  # incremental update (30-day GEO lookback)
    python scripts/update_data.py --full            # full GEO refresh
    python scripts/update_data.py --skip-geo        # skip GEO (API-heavy); run other sources
    python scripts/update_data.py --sources glass cgga tcga   # run only named sources
"""

import argparse
import logging
import sys
import time
from collections import Counter
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Project root resolution
# ---------------------------------------------------------------------------


def _resolve_project_root():
    """Find the project root by looking for data/ + requirements.txt."""
    script_path = Path(__file__).resolve()
    candidates = [
        script_path.parent.parent,
        script_path.parent,
        Path.cwd(),
    ]
    for candidate in candidates:
        if (candidate / "data").is_dir() and (candidate / "requirements.txt").is_file():
            return candidate
    return script_path.parent.parent


PROJECT_ROOT = _resolve_project_root()
DATA_FILE = PROJECT_ROOT / "data" / "datasets.json"

# Ensure the project root is on sys.path so that ``from scripts.utils ...``
# works regardless of the working directory.
_root_str = str(PROJECT_ROOT)
if _root_str not in sys.path:
    sys.path.insert(0, _root_str)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("update_data")

# ---------------------------------------------------------------------------
# Imports from local modules (after sys.path adjustment)
# ---------------------------------------------------------------------------

from scripts.utils import (  # noqa: E402
    deduplicate_datasets,
    load_existing_data,
    save_data,
    validate_dataset,
)
from scripts.sources.geo import fetch_geo_datasets  # noqa: E402
from scripts.sources.glass import fetch_glass_datasets  # noqa: E402
from scripts.sources.cgga import fetch_cgga_datasets  # noqa: E402
from scripts.sources.tcga import fetch_tcga_datasets  # noqa: E402
from scripts.sources.cptac import fetch_cptac_datasets  # noqa: E402
from scripts.sources.cbio import fetch_cbio_datasets  # noqa: E402
from scripts.sources.others import fetch_other_datasets  # noqa: E402

# ---------------------------------------------------------------------------
# Source registry
# ---------------------------------------------------------------------------

SOURCE_REGISTRY = {
    "geo": fetch_geo_datasets,
    "glass": fetch_glass_datasets,
    "cgga": fetch_cgga_datasets,
    "tcga": fetch_tcga_datasets,
    "cptac": fetch_cptac_datasets,
    "cbio": fetch_cbio_datasets,
    "others": fetch_other_datasets,
}

ALL_SOURCE_NAMES = list(SOURCE_REGISTRY.keys())

# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args():
    parser = argparse.ArgumentParser(
        description="Update the Recurrent Glioma Multi-Omics Explorer dataset cache.",
    )
    parser.add_argument(
        "--full",
        action="store_true",
        help="Full GEO refresh (ignore incremental lookback window).",
    )
    parser.add_argument(
        "--recent-days",
        type=int,
        default=30,
        help="GEO incremental lookback window in days (default: 30).",
    )
    parser.add_argument(
        "--skip-geo",
        action="store_true",
        help="Skip the GEO source (useful for quick non-API runs).",
    )
    parser.add_argument(
        "--sources",
        nargs="+",
        choices=ALL_SOURCE_NAMES,
        default=None,
        help="Run only the listed sources (e.g. --sources glass cgga tcga).",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Orchestration helpers
# ---------------------------------------------------------------------------


def _sources_to_run(args):
    """Determine which sources to run based on CLI arguments."""
    if args.sources:
        return args.sources
    sources = list(ALL_SOURCE_NAMES)
    if args.skip_geo and "geo" in sources:
        sources.remove("geo")
    return sources


def _run_source(name, fetcher, existing_ids, args):
    """Run a single source fetcher with error handling.

    Returns a list of dataset dicts (may be empty on failure).
    """
    logger.info("--- Running source: %s ---", name.upper())
    start = time.time()

    try:
        kwargs = {"existing_ids": existing_ids}
        if name == "geo":
            kwargs["full_refresh"] = args.full
            kwargs["recent_days"] = args.recent_days

        datasets = fetcher(**kwargs)
        elapsed = time.time() - start
        logger.info(
            "Source %s returned %d datasets in %.1f seconds",
            name.upper(),
            len(datasets),
            elapsed,
        )
        return datasets

    except Exception as exc:
        elapsed = time.time() - start
        logger.error(
            "Source %s failed after %.1f seconds: %s",
            name.upper(),
            elapsed,
            exc,
            exc_info=True,
        )
        return []


def _merge_datasets(existing, new_datasets):
    """Merge new datasets into the existing list (new entries take precedence)."""
    existing_map = {ds["id"]: ds for ds in existing}
    for ds in new_datasets:
        existing_map[ds["id"]] = ds  # upsert
    return list(existing_map.values())


def _validate_all(datasets):
    """Validate all datasets, logging warnings for invalid entries."""
    valid = []
    invalid_count = 0
    for ds in datasets:
        is_valid, missing = validate_dataset(ds)
        if is_valid:
            valid.append(ds)
        else:
            invalid_count += 1
            logger.warning(
                "Invalid dataset %s: missing fields %s",
                ds.get("id", "<no-id>"),
                missing,
            )
    if invalid_count:
        logger.warning("Dropped %d invalid datasets", invalid_count)
    return valid


def _sort_datasets(datasets):
    """Sort datasets by source then by publication_date descending."""
    def sort_key(ds):
        source = ds.get("source", "ZZZ")
        date = ds.get("publication_date", "")
        return (source, date)

    return sorted(datasets, key=sort_key, reverse=False)


def _print_summary(datasets):
    """Print summary statistics about the dataset collection."""
    logger.info("=" * 60)
    logger.info("DATASET SUMMARY")
    logger.info("=" * 60)
    logger.info("Total datasets: %d", len(datasets))

    # By source
    source_counts = Counter(ds.get("source", "Unknown") for ds in datasets)
    logger.info("By source:")
    for source, count in sorted(source_counts.items()):
        logger.info("  %-20s %d", source, count)

    # Total sample counts
    total_samples = sum(ds.get("sample_count", 0) for ds in datasets)
    total_recurrent = sum(ds.get("recurrent_sample_count", 0) or 0 for ds in datasets)
    logger.info("Total samples across all datasets: %d", total_samples)
    logger.info("Total recurrent samples (where known): %d", total_recurrent)

    # Data types
    dt_counts = Counter()
    for ds in datasets:
        for dt in ds.get("data_types", []):
            dt_counts[dt] += 1
    logger.info("Data types (across datasets):")
    for dt, count in dt_counts.most_common(15):
        logger.info("  %-30s %d", dt, count)

    # Tumor subtypes
    subtype_counts = Counter()
    for ds in datasets:
        for st in ds.get("tumor_subtypes", []):
            subtype_counts[st] += 1
    logger.info("Tumor subtypes (across datasets):")
    for st, count in subtype_counts.most_common(10):
        logger.info("  %-30s %d", st, count)

    logger.info("=" * 60)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    args = parse_args()
    logger.info("Recurrent Glioma Explorer - Data Update started at %s", datetime.now())
    logger.info("Project root: %s", PROJECT_ROOT)
    logger.info("Data file: %s", DATA_FILE)

    # Load existing data
    existing_data = load_existing_data(DATA_FILE)
    existing_ids = {ds.get("id", "") for ds in existing_data}
    logger.info("Loaded %d existing datasets", len(existing_data))

    # Determine which sources to run
    sources = _sources_to_run(args)
    logger.info("Sources to run: %s", ", ".join(s.upper() for s in sources))

    # Run each source and collect new datasets
    all_new = []
    for name in sources:
        fetcher = SOURCE_REGISTRY[name]
        new_datasets = _run_source(name, fetcher, existing_ids, args)
        all_new.extend(new_datasets)

    logger.info("Collected %d datasets from all sources", len(all_new))

    # Merge with existing
    merged = _merge_datasets(existing_data, all_new)
    logger.info("After merge: %d datasets", len(merged))

    # Deduplicate
    deduped = deduplicate_datasets(merged)
    logger.info("After deduplication: %d datasets", len(deduped))

    # Validate
    valid = _validate_all(deduped)
    logger.info("After validation: %d datasets", len(valid))

    # Sort
    final = _sort_datasets(valid)

    # Save
    save_data(final, DATA_FILE)
    logger.info("Saved %d datasets to %s", len(final), DATA_FILE)

    # Print summary
    _print_summary(final)

    logger.info("Data update complete at %s", datetime.now())


if __name__ == "__main__":
    main()
