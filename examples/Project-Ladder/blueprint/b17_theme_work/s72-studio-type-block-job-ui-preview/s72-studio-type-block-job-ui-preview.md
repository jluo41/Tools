s72 · Studio Type: Block Job UI Preview
=======================================
view: overview
emoji: 👀
band: s1N
name: Block Job UI Preview

**Stage:** shaping

**Holds:** One live preview per Block type: its Block page, a Job and a Task, as the server renders them.

**Title:** `sNN · Block Job UI Preview: <Block type>`

**Examples:** s11 · s12 · s13 · s14 · s15

**Topic:** This type defines the content of its Studio instances. Shared Blueprint bands are defined by `delivery/page-spec/studio-bands.json`. Other Work Blocks (Blueprint) reference this definition when they use this type and define only their own additional types.

**Feeds:** none



Decided
-------

- s72-D01 · Each Studio type is its own topic in the s7N Studio Type band (JL 261127: "I want each type of the studio should be a sperate markdown. and I want to put them as a group of studio in studio as well.")
