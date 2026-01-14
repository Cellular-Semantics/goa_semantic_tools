"""
Data Downloader Utility

Downloads and caches GO ontology and GAF annotation files.
Uses download-and-cache strategy to keep package lightweight.
"""
import gzip
import shutil
from pathlib import Path
from typing import Optional

import requests


def get_reference_data_dir() -> Path:
    """
    Get path to reference_data directory at repo root.

    Returns:
        Path to reference_data directory
    """
    # Navigate from this file to repo root
    current_file = Path(__file__)
    repo_root = current_file.parent.parent.parent.parent.parent
    ref_dir = repo_root / "reference_data"
    ref_dir.mkdir(exist_ok=True)
    return ref_dir


def get_test_data_dir() -> Path:
    """
    Get path to tests/test_data directory.

    Returns:
        Path to test_data directory
    """
    current_file = Path(__file__)
    repo_root = current_file.parent.parent.parent.parent.parent
    test_dir = repo_root / "tests" / "test_data"
    return test_dir


def _download_file(url: str, dest_path: Path, chunk_size: int = 8192) -> None:
    """
    Download file from URL to destination path with progress indication.

    Args:
        url: URL to download from
        dest_path: Destination file path
        chunk_size: Download chunk size in bytes (default: 8192)

    Raises:
        requests.RequestException: If download fails
    """
    print(f"Downloading {url}...")
    print(f"Destination: {dest_path}")

    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))
    downloaded = 0

    dest_path.parent.mkdir(parents=True, exist_ok=True)

    with open(dest_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)

                if total_size > 0:
                    percent = (downloaded / total_size) * 100
                    mb_downloaded = downloaded / (1024 * 1024)
                    mb_total = total_size / (1024 * 1024)
                    print(
                        f"  Progress: {percent:.1f}% ({mb_downloaded:.1f}/{mb_total:.1f} MB)",
                        end="\r",
                    )

    print(f"\n  Downloaded successfully: {dest_path.stat().st_size / (1024**2):.2f} MB")


def _decompress_gzip(gz_path: Path, output_path: Path) -> None:
    """
    Decompress a gzip file.

    Args:
        gz_path: Path to .gz file
        output_path: Path for decompressed output

    Raises:
        IOError: If decompression fails
    """
    print(f"Decompressing {gz_path.name}...")

    with gzip.open(gz_path, "rb") as f_in:
        with open(output_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

    print(
        f"  Decompressed successfully: {output_path.stat().st_size / (1024**2):.2f} MB"
    )


def ensure_go_data(force_download: bool = False) -> Path:
    """
    Ensure GO ontology file is available, downloading if necessary.

    Downloads go-basic.obo from GO PURL and caches in reference_data/.
    Skips download if file already exists unless force_download=True.

    Args:
        force_download: If True, download even if file exists (default: False)

    Returns:
        Path to cached go-basic.obo file

    Raises:
        requests.RequestException: If download fails
    """
    ref_dir = get_reference_data_dir()
    go_obo_path = ref_dir / "go-basic.obo"

    if go_obo_path.exists() and not force_download:
        print(f"GO ontology already cached: {go_obo_path}")
        print(f"  File size: {go_obo_path.stat().st_size / (1024**2):.2f} MB")
        return go_obo_path

    # Download from GO PURL
    url = "http://purl.obolibrary.org/obo/go/go-basic.obo"
    _download_file(url, go_obo_path)

    return go_obo_path


def ensure_gaf_data(species: str = "human", force_download: bool = False) -> Path:
    """
    Ensure GAF annotation file is available, downloading if necessary.

    Downloads GAF file from EBI QuickGO and caches in reference_data/.
    Automatically decompresses .gz file.
    Skips download if file already exists unless force_download=True.

    Args:
        species: Species name ("human" or "mouse") (default: "human")
        force_download: If True, download even if file exists (default: False)

    Returns:
        Path to cached decompressed GAF file

    Raises:
        ValueError: If species is not supported
        requests.RequestException: If download fails
        IOError: If decompression fails
    """
    if species not in ["human", "mouse"]:
        raise ValueError(f"Unsupported species: {species}. Must be 'human' or 'mouse'")

    ref_dir = get_reference_data_dir()
    gaf_path = ref_dir / f"goa_{species}.gaf"
    gaf_gz_path = ref_dir / f"goa_{species}.gaf.gz"

    if gaf_path.exists() and not force_download:
        print(f"GAF file already cached: {gaf_path}")
        print(f"  File size: {gaf_path.stat().st_size / (1024**2):.2f} MB")
        return gaf_path

    # Download from EBI
    species_upper = species.upper()
    url = f"http://ftp.ebi.ac.uk/pub/databases/GO/goa/{species_upper}/goa_{species}.gaf.gz"

    _download_file(url, gaf_gz_path)

    # Decompress
    _decompress_gzip(gaf_gz_path, gaf_path)

    # Optionally remove .gz file to save space
    # gaf_gz_path.unlink()

    return gaf_path


def get_test_gaf_path() -> Optional[Path]:
    """
    Get path to bundled test GAF subset.

    Returns:
        Path to test GAF file if it exists, None otherwise
    """
    test_dir = get_test_data_dir()
    test_gaf_path = test_dir / "goa_human_subset.gaf"

    if test_gaf_path.exists():
        return test_gaf_path

    return None
