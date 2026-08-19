# Q · the size of the files a Claude Code VS Code extension ships

On a macOS machine with the Claude Code VS Code extension installed, list the
extension directory — for example
`/Users/jluo41/.vscode/extensions/anthropic.claude-code-<version>-darwin-arm64`
— and report the byte size of each file it ships, at minimum:

- the webview bundle (`webview/index.js` or its equivalent)
- the extension host bundle (`extension.js`)
- the packed command-line executable under `resources/`
  (`native-binary/claude` or its equivalent)

Report the extension version measured, the exact command used, and the date. If
more than one version is installed, report every version present, so a reader can
see whether the sizes move between releases.

Deliverable: a QA digest plus a machine-readable listing of name, bytes, version.
Accepted: a size per file with the version and command named | a listed file is
absent in that release, stated as such.
