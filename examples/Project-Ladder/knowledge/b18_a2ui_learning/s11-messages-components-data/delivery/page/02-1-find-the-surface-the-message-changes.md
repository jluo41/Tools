# 1. Find the surface the message changes

**Every message names one surface, and does one thing to it.**

- 🆕 `createSurface`: opens the surface (`"flight-booking-surface"`)
- 🧱 `updateComponents`: lays out what is on it (Card › Column › FlightCard, Button)
- 🔢 `updateDataModel`: fills in the values (`/outbound/pax = 1`)
- 🗑️ `deleteSurface`: removes it

🔍 **Look for:** the `surfaceId` at the top of each message ([Resource 2](/_board/page?path=%2Fexamples%2FProject-Ladder%2Fknowledge%2Fb18_a2ui_learning%2Fs01-official-sources%2Fdelivery%2Flearning.md))

✅ **You know it when:** you can say which surface a message changes, and how.
