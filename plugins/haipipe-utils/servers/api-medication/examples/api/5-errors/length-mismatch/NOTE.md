# doses shorter than items

service: describe-medication
HTTP 422

422, not a silent zip truncation. Truncating would re-pair every row after the missing one onto the wrong drug, with no exception raised.
