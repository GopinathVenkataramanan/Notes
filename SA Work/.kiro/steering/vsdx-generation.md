---
inclusion: auto
name: vsdx-generation
description: Rules and known pitfalls for generating, editing, debugging or validating Visio .vsdx files (build_vsdx.py, validate_vsdx.py, diagrams folder). Use whenever a Visio file is created, changed, fails to open, or hangs.
---

# Visio (.vsdx) generation: reference context

This workspace generates Visio files from Python using only the standard library. Visio is strict and fails silently: a malformed file either shows "file is corrupt" or makes Visio hang on open with no error. Follow these rules and always validate before handing a file back.

## Files

- Generator: `tools/build_vsdx.py`. It writes `diagrams/SaaS_Replacement_Discovery_Pack.vsdx` and SVG previews to `diagrams/preview/`.
- Validator: `tools/validate_vsdx.py`. It exits with 1 on any ERROR.
- Known-good reference saved by Visio: `reference/virtual-desktop-get-started-diagram.vsdx`. Treat it as the ground truth whenever you are unsure how Visio writes something. Unzip it and inspect it with Python `zipfile`.
- Requires Python 3.12+, because `build_vsdx.py` uses backslash-escaped quotes inside f-string expressions.

## Mandatory workflow

1. Edit `tools/build_vsdx.py`. Never hand-edit the .vsdx.
2. `python tools\build_vsdx.py`
3. `python tools\validate_vsdx.py --compare reference\virtual-desktop-get-started-diagram.vsdx`
4. Expect `0 error(s), 0 warning(s)`. The only accepted compare gap is the theme part and relationship, which is optional because shapes use explicit colours.
5. If the validator passes but Visio still fails, diff the failing part against the same part in the reference, then add a validator rule for the new failure mode.

## Hard rules learned the hard way

| Rule | What happens if broken |
|---|---|
| `visio/document.xml` must contain `DocumentSettings`, `Colors`, `FaceNames`, `StyleSheets` and `DocumentSheet`, in that order | Visio reports the file as corrupt |
| StyleSheet `ID="0"` ("No Style") is the root and must have NO `LineStyle`/`FillStyle`/`TextStyle` attributes | Self-reference makes Visio hang (Not Responding) |
| No style inheritance cycles. Every referenced style ID must exist | Hang or corrupt |
| Shapes point at style `3` ("Normal", which inherits from 0). `DocumentSettings Default*Style` = 3 | Unresolved formatting |
| `ColorEntry IX` 0-23 are built-in palette slots. Custom entries start at 24 | Corrupt or wrong colours |
| `FaceName` has no `ID` attribute and uses real `UnicodeRanges`/`CharSets`/`Panose` values (copy from the reference). Fonts are referenced by name, e.g. `<Cell N="Font" V="Calibri"/>` | Font matching fails |
| Every part has a content type in `[Content_Types].xml`, and every rel target exists | Corrupt |
| Include `visio/windows.xml`, `docProps/core.xml` and `docProps/app.xml`, as Visio always writes them | Less tolerant open path |
| PageSheet carries `PageScale`/`DrawingScale` (`U="IN_F"`) plus the standard page cells | Scaling issues |
| Geometry starts with `MoveTo`, `RelMoveTo`, `Ellipse` or `InfiniteLine`. Row `IX` values are unique | Shape not drawn or corrupt |
| Shape IDs are unique per page, including nested shapes. `Master=` must exist in `masters.xml` | Corrupt |
| Escape all text with `xml.sax.saxutils.escape`. No control characters | XML parse failure |

## Package skeleton the generator must produce

```
[Content_Types].xml
_rels/.rels                         -> document, core-properties, extended-properties
docProps/core.xml, docProps/app.xml
visio/document.xml
visio/_rels/document.xml.rels       -> pages, windows
visio/windows.xml
visio/pages/pages.xml
visio/pages/_rels/pages.xml.rels    -> pageN.xml
visio/pages/pageN.xml
```

Namespaces:
- Visio main: `http://schemas.microsoft.com/office/visio/2012/main`
- Visio relationships: `http://schemas.microsoft.com/visio/2010/relationships`
- OPC relationships: `http://schemas.openxmlformats.org/package/2006/relationships`

## Coordinate system

Visio Y grows upwards from the bottom-left in inches. The generator authors in top-left coordinates and converts with `PH - y - h`. `PinX`/`PinY` give the shape centre and `LocPin*` is half of the width/height. Line geometry is relative to the shape's own bounding box.

## Validator notes

- `Themed` is a legitimate cell value in Visio-saved files.
- Shapes with `Master` or `MasterShape` (and their sub-shapes) inherit cells, so omitted PinX/Width and partial geometry are fine there.
- 1-D shapes (those with `BeginX`) can have negative Width/Height.
- When adding a rule, run it against the reference file too. It must still report 0 errors there, so you catch false positives.
