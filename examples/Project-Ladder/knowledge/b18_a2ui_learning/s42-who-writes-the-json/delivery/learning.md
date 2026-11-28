# Who Writes the JSON?

## The question

> "so the JSON is return by our Agent, or our Agent still just return the text, and a post processing turn the text to the JSON?" (2026-11-27)

## Short answer

In between. The model still writes text, but in a fixed format, A2UI Express, between `<a2ui>` and `</a2ui>` tags.
The Agent SDK's compiler, running on your agent's server, parses that block, checks it against the catalog and emits
the JSON messages. It is not free prose guessed into JSON afterwards. The model may also write the wire JSON
directly; Express is shorter.

## What the model writes

The skill the SDK generates teaches the model the grammar and the catalog's components. For the flight request it
streams:

```text
<a2ui>
$/outbound/pax = 1
$/outbound/price = 455
$/return/pax = 2
$/return/price = 970
root = Card(Column([
  FlightCard(flightNumber="LH 454", origin="BER", destination="SFO", price=$/outbound/price, passengers=$/outbound/pax),
  FlightCard(flightNumber="UA 901", origin="SFO", destination="BER", price=$/return/price, passengers=$/return/pax),
  Button(Text("Confirm booking"), variant="primary", action=Event("confirm_booking", {outboundPax: $/outbound/pax, returnPax: $/return/pax}))
]))
</a2ui>
```

Lines starting with `$/` set values in the data model; `root = ...` is the component tree.

## What the compiler does

It parses the block, rejects a component or property the catalog does not allow, gives every component an ID and
splits the result into messages: `createSurface`, then `updateComponents` for the layout and `updateDataModel` for the
values.


## The three JSON messages, in full

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

## What the client receives

Only the JSON messages. The renderer never sees Express; it builds the surface from the messages and the data model.

## Try explaining

Take one line of the Express block, such as `$/return/pax = 2`, and find where it ends up in the three JSON messages.
