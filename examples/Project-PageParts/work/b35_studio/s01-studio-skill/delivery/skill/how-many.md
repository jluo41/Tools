How many sNN per level
----------------------

At most **9 sNN at a Block, 5 at a Job, 3 at a Task** (`new_topic.py` `LIMITS`). This counts topic folders at that
level, not the largest number: s51 can be one of a Block's nine. Keep each topic about one delivery. Before adding one
past the limit, reuse a related topic, put it on the Job or Task that uses its delivery, or split the level; existing
topics keep their ids and files. A topic is numbered free across the whole Block (Block, Jobs and Tasks share one sNN
numbering).
