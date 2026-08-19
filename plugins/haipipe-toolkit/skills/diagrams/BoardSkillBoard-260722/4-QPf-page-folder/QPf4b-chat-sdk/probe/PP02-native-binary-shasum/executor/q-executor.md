# Q · the identity of the command-line executable packed inside the VS Code extension

The Claude Code VS Code extension ships a compiled command-line executable under
its `resources/` directory. A standalone installation of the same product keeps
its releases under `~/.local/share/claude/versions/<version>`.

For one version present in both places on this machine:

- compute `shasum -a 256` of the packed executable and of the standalone release
  of that same version, and report both digests verbatim
- report the version, the two full paths, the command and the date
- report what the `claude` executable on the PATH resolves to, and whether it is
  the same file as the standalone release compared above

Deliverable: a QA digest carrying both digests verbatim.
Accepted: identical | different, with the differing digests shown | no version is
present in both places on this machine, stated as such.
