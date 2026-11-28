# The three JSON messages, in full

These are the official v1.0 messages for the flight example, from the "Messages on the wire" section of the A2UI
overview (Resource 2; Apache-2.0). Component IDs are chosen by the compiler; these are for readability.

**Surface creation**, `createSurface`:

```json
{
  "version": "1.0",
  "createSurface": {
    "surfaceId": "flight-booking-surface",
    "catalogId": "https://example.com/catalogs/travel/v1/catalog.json"
  }
}
```

**Layout**, `updateComponents`: each component names its children by ID, starting from `root`; prices and passenger
counts are paths into the data model (`{"@path": "/return/pax"}`).

```json
{
  "version": "1.0",
  "updateComponents": {
    "surfaceId": "flight-booking-surface",
    "components": [
      {"id": "root", "component": "Card", "child": "layout_col"},
      {
        "id": "layout_col",
        "component": "Column",
        "children": ["flight_outbound", "flight_return", "submit_btn"]
      },
      {
        "id": "flight_outbound",
        "component": "FlightCard",
        "flightNumber": "LH 454",
        "origin": "BER",
        "destination": "SFO",
        "price": {"@path": "/outbound/price"},
        "passengers": {"@path": "/outbound/pax"}
      },
      {
        "id": "flight_return",
        "component": "FlightCard",
        "flightNumber": "UA 901",
        "origin": "SFO",
        "destination": "BER",
        "price": {"@path": "/return/price"},
        "passengers": {"@path": "/return/pax"}
      },
      {"id": "submit_label", "component": "Text", "text": "Confirm booking"},
      {
        "id": "submit_btn",
        "component": "Button",
        "child": "submit_label",
        "variant": "primary",
        "action": {
          "event": {
            "name": "confirm_booking",
            "context": {
              "outboundPax": {"@path": "/outbound/pax"},
              "returnPax": {"@path": "/return/pax"}
            }
          }
        }
      }
    ]
  }
}
```

**Values**, `updateDataModel`: the numbers the paths point to.

```json
{
  "version": "1.0",
  "updateDataModel": {
    "surfaceId": "flight-booking-surface",
    "path": "/",
    "value": {
      "outbound": {"pax": 1, "price": 455},
      "return": {"pax": 2, "price": 970}
    }
  }
}
```
