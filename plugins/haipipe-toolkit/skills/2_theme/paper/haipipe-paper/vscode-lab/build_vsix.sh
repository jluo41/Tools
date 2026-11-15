#!/usr/bin/env bash
# Package this folder as a .vsix by hand (no npm): the manifest, the content types, and extension/.
# Usage: build_vsix.sh [out.vsix]   then the author installs it once: code --install-extension <out.vsix>
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
out="${1:-$here/paper-lab.vsix}"
tmp="$(mktemp -d)"
mkdir -p "$tmp/extension"
cp "$here/package.json" "$here/extension.js" "$tmp/extension/"
cat > "$tmp/[Content_Types].xml" <<'XML'
<?xml version="1.0" encoding="utf-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension=".json" ContentType="application/json"/><Default Extension=".js" ContentType="application/javascript"/><Default Extension=".vsixmanifest" ContentType="text/xml"/></Types>
XML
cat > "$tmp/extension.vsixmanifest" <<'XML'
<?xml version="1.0" encoding="utf-8"?>
<PackageManifest Version="2.0.0" xmlns="http://schemas.microsoft.com/developer/vsx-schema/2011" xmlns:d="http://schemas.microsoft.com/developer/vsx-schema-design/2011">
  <Metadata>
    <Identity Language="en-US" Id="paper-lab" Version="0.3.0" Publisher="haipipe" />
    <DisplayName>Paper Writing Lab</DisplayName>
    <Description xml:space="preserve">Opens each Section draft page above and its session terminal below.</Description>
    <Tags></Tags>
    <Categories>Other</Categories>
    <GalleryFlags>Public</GalleryFlags>
    <Properties>
      <Property Id="Microsoft.VisualStudio.Code.Engine" Value="^1.80.0" />
      <Property Id="Microsoft.VisualStudio.Code.ExtensionDependencies" Value="" />
      <Property Id="Microsoft.VisualStudio.Code.ExtensionPack" Value="" />
      <Property Id="Microsoft.VisualStudio.Code.ExtensionKind" Value="workspace" />
      <Property Id="Microsoft.VisualStudio.Code.LocalizedLanguages" Value="" />
    </Properties>
  </Metadata>
  <Installation><InstallationTarget Id="Microsoft.VisualStudio.Code"/></Installation>
  <Dependencies/>
  <Assets><Asset Type="Microsoft.VisualStudio.Code.Manifest" Path="extension/package.json" Addressable="true" /></Assets>
</PackageManifest>
XML
rm -f "$out"
(cd "$tmp" && zip -qr "$out" "[Content_Types].xml" extension.vsixmanifest extension)
rm -rf "$tmp"
echo "$out"
