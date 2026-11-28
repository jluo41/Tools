# Short answer

In between. The model still writes text, but in a fixed format, A2UI Express, between `<a2ui>` and `</a2ui>` tags.
The Agent SDK's compiler, running on your agent's server, parses that block, checks it against the catalog and emits
the JSON messages. It is not free prose guessed into JSON afterwards. The model may also write the wire JSON
directly; Express is shorter.
