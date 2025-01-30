import os
import glob
import re
import datetime

# Directories
SQL_DIR = "data/sql/"
CSV_DIR = "data/csv/"

# Ensure output directory exists
os.makedirs(CSV_DIR, exist_ok=True)

# Get today's date
today_date = datetime.datetime.now().strftime("%Y-%m-%d")

def get_latest_sql_file(pattern):
    """Find the latest SQL file matching the given pattern."""
    sql_files = sorted(glob.glob(os.path.join(SQL_DIR, pattern)), key=os.path.getctime, reverse=True)
    if not sql_files:
        print(f"❌ No SQL files found for {pattern}")
        return None
    latest_sql = sql_files[0]
    print(f"✅ Latest SQL file found: {latest_sql}")
    return latest_sql

def extract_page_titles():
    """Extract Wikipedia page ID → title mappings from page.sql."""
    page_file = get_latest_sql_file("page.sql")
    if not page_file:
        return {}

    page_id_to_title = {}
    with open(page_file, "r", encoding="utf-8") as infile:
        for line in infile:
            matches = re.findall(r"\((\d+),0,'(.*?)'", line)  # Extract (ID, Title)
            for page_id, title in matches:
                page_id_to_title[page_id] = title.replace("_", " ")  # Convert underscores to spaces

    print(f"✅ Extracted {len(page_id_to_title)} Wikipedia page titles.")
    return page_id_to_title

def sql_to_csv():
    """Convert Wikipedia pagelinks SQL file to CSV using page titles."""
    pagelinks_file = get_latest_sql_file("wikipedia_pagelinks.sql")
    if not pagelinks_file:
        return

    output_file = os.path.join(CSV_DIR, f"wikipedia_links_{today_date}.csv")
    page_id_to_title = extract_page_titles()

    link_count = 0
    with open(pagelinks_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write("source,target\n")  # CSV Header
        for line in infile:
            matches = re.findall(r"\((\d+),0,(\d+)\)", line)  # Extract (Source ID, Target ID)
            for source_id, target_id in matches:
                source_title = page_id_to_title.get(source_id, None)
                target_title = page_id_to_title.get(target_id, None)

                if source_title and target_title:
                    print(f"📝 Extracted: {source_title} -> {target_title}")  # Debugging
                    outfile.write(f"{source_title},{target_title}\n")
                    link_count += 1

    if link_count == 0:
        print("⚠️ No valid links extracted! Check if `page.sql` is correct.")
    else:
        print(f"✅ Extracted {link_count} Wikipedia links to {output_file}")

    # 🚨 DELETE SQL FILES AFTER PROCESSING
    delete_sql_files()

def delete_sql_files():
    """Delete SQL files after processing."""
    sql_files = ["data/sql/wikipedia_pagelinks.sql", "data/sql/page.sql"]
    for sql_file in sql_files:
        if os.path.exists(sql_file):
            os.remove(sql_file)
            print(f"🗑 Deleted {sql_file}")

if __name__ == "__main__":
    sql_to_csv()
