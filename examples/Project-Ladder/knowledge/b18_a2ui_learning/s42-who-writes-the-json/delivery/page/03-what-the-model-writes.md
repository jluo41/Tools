# What the model writes

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
