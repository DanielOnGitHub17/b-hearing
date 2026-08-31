# B-Hearing Server

This project contains the backend for the B-Hearing application and includes data processing scripts for the KJV text import workflow.

## Project overview

The server is a Django application with support for:

- Bible/selection data import and processing
- Database-backed reading and selection logic
- API-style endpoints for app interactions
- Local development and data population scripts

## Data import workflow

The following notes describe the KJV data extraction and curation process used to prepare the JSON bible data.

### Gutenberg extraction notes

A JavaScript snippet used to extract chapter text from the Gutenberg page:

```javascript
JSON.stringify($$(".chapter").map(
  i => [...i.getElementsByTagName("p")].map(
    j => j.textContent.trim().replaceAll('\n', ' ')
  )
))
```

Example output:

```text
"5:6 And Seth lived an hundred and five years, and begat Enos: 5:7 And Seth lived after he begat Enos eight hundred and seven years, and begat sons and daughters: 5:8 And all the days of Seth were nine hundred and twelve years: and he died."
```

Notes:

- Verse text may be split across lines and must be normalized.
- Some entries need manual cleanup or re-labeling after extraction.
- There were many connected verses without a label; these were adjusted in VS Code.
- The curated process yielded the final KJV JSON dataset.

### Post-processing notes

When cleaning the extracted data, the following replacement was used in VS Code:

```text
",\n *"([a-z .])
```

Replace with:

```text
  $1
```

This was applied to the verse blocks that did not have an explicit label.

### Bible totals

- Number of books in KJV: 66
- Number of chapters in KJV: 1189
- Total verses in KJV: 31,102
- Final curated file size / line count after processing: around 33,614 lines

### Run the data population script

```bash
python manage.py shell
from selections import populate
populate.process_pg_json()
```

On Windows, the shell command may be run as:

```bash
python manage.py shell
```

## API testing

For HTTP request examples, see [curl-and-http.md](curl-and-http.md).

## Project notes

This README is intentionally kept more readable and focused on setup and data workflow. More detailed request patterns are maintained in [curl-and-http.md](curl-and-http.md).