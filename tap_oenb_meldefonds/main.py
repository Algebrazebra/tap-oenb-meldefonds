import csv
import requests
import singer

from datetime import datetime, timezone

LOGGER = singer.get_logger()

OEKB_URL = "https://my.oekb.at/kms-reporting/public?report=steuerdaten-liste-mf-gesamt&format=CSV"

MELDEFONDS_SCHEMA = {
    "properties": {
        "ISIN": {
            "type": "string",
            "pattern": "[A-Z]{2}[A-Z0-9]{9}[0-9]",
            "minLength": 12,
            "maxLength": 12,
        },
        "Bezeichnung": {"type": "string"},
        "Steuerlicher Vertreter": {"type": "string"},
        "KEst-Meldefonds seit": {"type": "string"},
        "Absichtserklärung": {"type": "string"},
        "Art gemäß FMV 2015": {
            "type": "string",
            "pattern": "\\d{1,2}\\.\\d{1,2}\\.\\d{4}",
            "minLength": 10,
            "maxLength": 10,
        },
        "Fondsstatus": {"type": "string"},
        "Ertragsverwendung": {"type": "string"},
        "Währung": {"type": "string"},
        "Fondsende": {
            "type": "string",
            "pattern": "\\d{1,2}\\.\\d{1,2}\\.\\d{4}",
            "minLength": 10,
            "maxLength": 10,
        },
    }
}


def download_meldefonds_data() -> str:
    """Download a .csv file of all Meldefonds data from the OEKB website."""
    with requests.Session() as session:
        session.headers.update({"user-agent": ""})
        response = session.get(OEKB_URL)
        decoded_content = response.content.decode()
    return decoded_content


def main() -> None:
    """Download Meldefonds data and export them via Singer."""
    now = datetime.now(timezone.utc).isoformat()
    meldefonds_data = download_meldefonds_data()
    meldefonds_csv = csv.DictReader(meldefonds_data.splitlines(), delimiter=";")
    meldefonds_records = [dict(f, timestamp=now) for f in list(meldefonds_csv)]
    singer.write_schema("Meldefonds", MELDEFONDS_SCHEMA, key_properties=["ISIN"])
    singer.write_records("Meldefonds", meldefonds_records)


if __name__ == "__main__":
    main()
