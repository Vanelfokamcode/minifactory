import duckdb
import httpx
import gzip
import csv
import io

S3_URL = "https://openfoodfacts-ds.s3.eu-west-3.amazonaws.com/en.openfoodfacts.org.products.csv.gz"

COLUMNS = [
    "code", "product_name", "brands_tags", "countries_en",
    "additives_n", "additives_tags", "nutriscore_grade",
    "nova_group", "completeness"
]

LIMIT = 50_000


def ingest():
    con = duckdb.connect("data/minifactory.duckdb")

    con.execute("DROP TABLE IF EXISTS raw_products")
    con.execute("""
        CREATE TABLE raw_products (
            code VARCHAR,
            product_name VARCHAR,
            brands_tags VARCHAR,
            countries_en VARCHAR,
            additives_n INTEGER,
            additives_tags VARCHAR,
            nutriscore_grade VARCHAR,
            nova_group INTEGER,
            completeness FLOAT
        )
    """)

    print("Téléchargement en cours...")
    response = httpx.get(S3_URL, follow_redirects=True, timeout=120)
    print(f"Téléchargé : {len(response.content)} octets")

    rows = []
    with gzip.open(io.BytesIO(response.content)) as gz:
        text_stream = io.TextIOWrapper(gz, encoding="utf-8", errors="replace")
        reader = csv.DictReader(text_stream, delimiter="\t")

        for i, row in enumerate(reader):
            if i >= LIMIT:
                break
            if i % 10000 == 0:
                print(f"  {i} lignes lues...")
            rows.append({col: row.get(col) or None for col in COLUMNS})

    print(f"{len(rows)} lignes lues, insertion en cours...")

    con.executemany("""
        INSERT INTO raw_products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, [
        [
            r["code"], r["product_name"], r["brands_tags"], r["countries_en"],
            int(r["additives_n"]) if r["additives_n"] else None,
            r["additives_tags"],
            r["nutriscore_grade"],
            int(r["nova_group"]) if r["nova_group"] else None,
            float(r["completeness"]) if r["completeness"] else None
        ]
        for r in rows
    ])

    print(f"Done. {len(rows)} lignes dans raw_products.")
    con.close()


if __name__ == "__main__":
    ingest()
