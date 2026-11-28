"""delivery_publish.py: [publish], the shared copies of a build. build_delivery.py runs this file inside its own
namespace (_load_part), so CFG, OUT, HERE, ENGINE_DIR, BUILD_WARNINGS, rel, _doc_parts, re, os, sys, shutil and
datetime come from there."""


def publish(previous: dict) -> dict:
    """[publish] (paper-build.toml): copy the delivered files into a round's clean/ after every build (ScalingGlucose
    and Pp-AgreeableRx 261122: a flat shared folder was made twice the same night; JL: "should we have the code to
    do this check?"); any other folder copies nothing and says why. Before: a shared folder after every build (JL 261023: "the
    delivery will be rendered here ... we will keep rendering it"), e.g. a OneDrive or SharePoint folder the co-authors
    open. `dir` is relative to the SPACE root (the folder with env.sh) or absolute; `files` maps an [outputs] key to
    the name it gets there. The last copy delivered is kept in <delivery>/.published/; a shared copy whose text or
    comments differ from it was edited by a co-author, so it is never overwritten: the new render is written beside it
    as "<name> (new render)", one file replaced by each build, and the build says so. A copy OneDrive holds online
    only (not downloaded) cannot be read, so it counts as changed too. Returns what was written."""
    pub = CFG.get("publish")
    if not isinstance(pub, dict) or not pub.get("dir"):
        return {}
    space = next((q for q in [HERE.resolve(), *HERE.resolve().parents] if (q / "env.sh").is_file()), HERE.resolve())
    dest = Path(os.path.expanduser(pub["dir"]))
    dest = dest if dest.is_absolute() else space / dest
    if not dest.is_dir():
        BUILD_WARNINGS.append(f"publish: folder not found, nothing copied: {pub['dir']}")
        return {}
    if not (dest.name == "clean" and re.fullmatch(r"Round\d+-v\d{4}", dest.parent.name)):
        BUILD_WARNINGS.append(f"❗ publish refused, nothing copied: {pub['dir']} is not a round's clean/ folder. A shared "
                              "folder is RoundN-vMMDD/ (hai-delivery ref/round-folder.md): word_round.py adopt-round "
                              "<flat-dir> or open-round, then [publish] dir = \".../RoundN-vMMDD/clean\"")
        return {}
    loose = [n for n in (pub.get("files") or {}).values() if not re.fullmatch(r"\d+-.+-v\d{4}-.+-clean\.(docx|pdf)", n)]
    if loose:   # -clean: never the working file's name, so nobody edits the clean copy for it (AgreeableJama 261123)
        BUILD_WARNINGS.append(f"❗ publish refused, nothing copied: clean/ names are N-<Name>-vMMDD-<kind>-clean: {', '.join(loose)}")
        return {}
    kept = HERE / ".published"
    kept.mkdir(exist_ok=True)
    done = {}
    for key, name in (pub.get("files") or {}).items():
        src = rel(OUT[key]) if OUT.get(key) else None
        if src is None or not src.is_file():
            BUILD_WARNINGS.append(f"publish: {key} was not built, {name} not copied")
            continue
        target, last = dest / name, kept / name
        if target.exists() and not (last.is_file() and _doc_parts(target) == _doc_parts(last)):
            target = dest / f"{Path(name).stem} (new render){Path(name).suffix}"   # one file, replaced each build
            BUILD_WARNINGS.append(f"publish: {name} in the shared folder differs from the last render (edited there?); "
                                  f"kept it, wrote {target.name}")
        shutil.copyfile(src, target)
        if target.name == name:
            shutil.copyfile(src, last)
            done[name] = {"from": OUT[key], "at": datetime.now().isoformat(timespec="seconds")}
        print(f"published {key} -> {target.name}")
    if done:   # the round's clean/ marker, written by the round tool's own writer
        sys.path.insert(0, str(ENGINE_DIR.parents[3] / "1_base/project/hai-delivery/scripts"))
        from word_round_folder import marker
        marker(dest, "The LaTeX PDF and the LaTeX-made Word of each file, no marks; rebuilt when the top changes.")
    return done
