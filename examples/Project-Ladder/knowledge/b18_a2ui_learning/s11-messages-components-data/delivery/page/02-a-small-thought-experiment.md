# A small thought experiment

Imagine a trip card with a passenger count. The card's component definition establishes where the count appears. The data model holds the count itself. Increasing it from one to two changes the value; it need not change the card's identity.

This is a conceptual example, not a captured Run or a complete protocol payload.

| Question | Look at |
|---|---|
| Which interface changes? | Surface ID |
| Which widget and position? | Component IDs and relationships |
| Which value is displayed? | Data path and current value |
| Which widgets are allowed? | The application's catalog |
