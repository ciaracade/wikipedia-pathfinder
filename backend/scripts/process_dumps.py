import os
import glob
import shutil
import datetime
import gzip
import requests
from bs4 import BeautifulSoup

# Define directories
DUMPS_DIR = "data/dumps/"
SQL_DIR = "data/sql/"
LAST_DUMP_FILE = "data/last_downloaded.txt"

# Wikipedia Dump URL
WIKI_DUMP_URL = "https://dumps.wikimedia.org/enwiki/latest/"

# Ensure directories exist
os.makedirs(DUMPS_DIR, exist_ok=True)
os.makedirs(SQL_DIR, exist_ok=True)

# Get today's date (YYYY-MM-DD)
today_date = datetime.datetime.now().strftime("%Y-%m-%d")

def get_latest_dump_url(file_keyword):
    """Find the latest Wikipedia dump URL for a specific file (pagelinks.sql.gz or page.sql.gz)."""
    response = requests.get(WIKI_DUMP_URL)
    if response.status_code != 200:
        print("❌ Failed to access Wikipedia Dumps site.")
        return None, None

    soup = BeautifulSoup(response.text, "html.parser")

    # Find the latest dump file containing the keyword
    for link in soup.find_all("a"):
        href = link.get("href")
        if href and file_keyword in href:
            full_url = WIKI_DUMP_URL + href
            dump_version = href.split("-")[-1]  # Extract version
            print(f"✅ Found latest {file_keyword} dump: {full_url} (Version: {dump_version})")
            return full_url, dump_version

    print(f"❌ No {file_keyword} dump found.")
    return None, None

def get_last_downloaded_version():
    """Read the last downloaded version from a file."""
    if os.path.exists(LAST_DUMP_FILE):
        with open(LAST_DUMP_FILE, "r") as f:
            return f.read().strip()
    return None

def save_latest_version(dump_version):
    """Save the latest downloaded version to a file."""
    with open(LAST_DUMP_FILE, "w") as f:
        f.write(dump_version)

def download_latest_dump(file_keyword):
    """Download the latest Wikipedia dump for pagelinks.sql.gz or page.sql.gz."""
    latest_dump_url, dump_version = get_latest_dump_url(file_keyword)
    if not latest_dump_url or not dump_version:
        return None, None

    last_downloaded_version = get_last_downloaded_version()

    if last_downloaded_version == dump_version:
        print(f"✅ Wikipedia dump {file_keyword} is already up to date. (Version: {dump_version})")
        return None, None  # No need to re-download

    dump_filename = f"{file_keyword}_{today_date}.sql.gz"
    dump_path = os.path.join(DUMPS_DIR, dump_filename)

    print(f"⬇️ Downloading {file_keyword} dump: {dump_path}...")
    response = requests.get(latest_dump_url, stream=True)
    if response.status_code == 200:
        with open(dump_path, "wb") as file:
            shutil.copyfileobj(response.raw, file)
        print(f"✅ Downloaded {file_keyword} dump: {dump_path}")

        return dump_path, dump_version
    else:
        print(f"❌ Failed to download {file_keyword}.")
        return None, None

def extract_gzip_to_sql(gz_file, output_filename):
    """Extract a .gz Wikipedia dump to SQL format."""
    if not gz_file:
        return None

    sql_path = os.path.join(SQL_DIR, output_filename)

    with gzip.open(gz_file, 'rt', encoding='utf-8') as gz_file_obj, open(sql_path, 'w', encoding='utf-8') as sql_file:
        shutil.copyfileobj(gz_file_obj, sql_file)

    print(f"✅ Extracted SQL file: {sql_path}")
    return sql_path

def keep_last_n_dumps(n=2):
    """Keep only the last N dumps and delete older ones, but always keep at least one."""
    dump_files = sorted(glob.glob(os.path.join(DUMPS_DIR, "*.gz")), key=os.path.getctime, reverse=True)
    
    # Keep at least one dump file
    if len(dump_files) > n:
        old_dumps = dump_files[n:]  # Keep the latest N, remove the rest
        for old_dump in old_dumps:
            os.remove(old_dump)
            print(f"🗑 Deleted old dump: {old_dump}")
    
    sql_files = sorted(glob.glob(os.path.join(SQL_DIR, "*.sql")), key=os.path.getctime, reverse=True)

    if len(sql_files) > n:
        old_sqls = sql_files[n:]  # Keep the latest N, remove the rest
        for old_sql in old_sqls:
            os.remove(old_sql)
            print(f"🗑 Deleted old SQL file: {old_sql}")

def main():
    """Download and process Wikipedia dumps while keeping the latest valid version."""
    success = False

    # Download and process pagelinks.sql.gz (links)
    pagelinks_gz, pagelinks_version = download_latest_dump("pagelinks.sql.gz")
    if pagelinks_gz:
        extract_gzip_to_sql(pagelinks_gz, "wikipedia_pagelinks.sql")
        success = True

    # Download and process page.sql.gz (page titles)
    page_gz, page_version = download_latest_dump("page.sql.gz")
    if page_gz:
        extract_gzip_to_sql(page_gz, "page.sql")
        success = True

    # If we successfully downloaded new dumps, update the version file and clean old dumps
    if success:
        save_latest_version(pagelinks_version or page_version)
        keep_last_n_dumps()

if __name__ == "__main__":
    main()
