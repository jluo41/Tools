# TODO — finish the `haipipe-discover` -> `haipipe-discovery` rename (cross-layer)

The discovery skill was renamed `haipipe-discover` -> `haipipe-discovery`
(commit `1e53ddb`, v1.8.0) to match the `haipipe-<noun>` sibling convention
(probe / paper / task / insight / project / application). The **discovery layer
itself + its project-level `.claude/skills` symlink are fully done.**

These OTHER layers still reference the OLD name. Every hit is a plain reference
(command example or dispatch mention) — no logic change. Just swap the token:

```
/haipipe-discover   ->  /haipipe-discovery
haipipe-discover    ->  haipipe-discovery
```

Paths below are relative to `plugins/haipipe-toolkit/`. Safe per-file command
(negative lookahead so it never double-writes an already-correct name):

```
perl -i -pe 's/haipipe-discover(?!y)/haipipe-discovery/g' <file>
```

## paper  (do in the paper session)
- [ ] `skills/paper/haipipe-paper/SKILL.md`  (L318)
- [ ] `skills/paper/ref/paper-lifecycle.md`  (L80)
- [ ] `skills/paper/ref/lifecycle-map.md`  (L15)
- [ ] `skills/paper/ref/delivery-need.md`  (L44)
- [ ] `skills/paper/1-lifecycle/haipipe-paper-seed/SKILL.md`  (L93, L106)
- [ ] `skills/paper/1-lifecycle/haipipe-paper-claims/SKILL.md`  (L90, L102)

## probe  (do in the probe session)
- [ ] `skills/probe/DESIGN.md`  (L206, L398)
- [ ] `skills/probe/haipipe-probe/ref/probe-attach.md`  (L27, L201)
- [ ] `skills/probe/haipipe-probe/ref/lifecycle-map.md`  (L13)

## application
- [ ] `skills/application/haipipe-application/ref/delivery-need.md`  (L45)

## task
- [ ] `skills/task/DESIGN.md`  (L34)

## toolkit root
- [ ] `README.md`  (L26)

---

Or sweep everything at once, run from `plugins/haipipe-toolkit/`:

```
grep -rl "haipipe-discover" skills README.md \
  | grep -v "skills/discovery/" \
  | xargs perl -i -pe 's/haipipe-discover(?!y)/haipipe-discovery/g'
```

Done when this returns nothing but historical changelog/decision-log mentions:

```
grep -rn "haipipe-discover" skills README.md | grep -v haipipe-discovery
```

Then delete this file.
