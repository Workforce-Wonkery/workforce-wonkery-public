# Practice navigation release

Practice now starts with six work topics and one catalogue of 112 existing public resources. Existing URLs and substantive guidance stay intact. This is a navigation release, not a source review or new policy interpretation.

## Publication manifest

After public review and CI, import approved source through the private import workflow. The Publisher must snapshot and check current target content before these writes, verify exact readback, and retain a rollback receipt:

| WordPress target | Source |
|---|---|
| Page 935 /practice/ | src/wordpress/templates/practice-editorial-v2.html |
| Page 1212 /practice/topics/ | src/wordpress/templates/practice-topic-library.html |
| Page 1211 /practice/tools/ | src/wordpress/templates/practice-resource-directory.html |
| Page 1387 /practice/quickstarts/ | src/wordpress/templates/practice-quickstarts.html |
| Template part assembler//header | Append the PRACTICE NAVIGATION START/END block from src/wordpress/template-parts/header-editorial-blocks.html to the freshly fetched live header. Preserve unrelated header changes. |

No subscriber email. No redirects or changes to policy claims. The enhancement applies only to Practice routes and the catalogue's named public resources. Existing course progress and specialist tools remain under their existing owners.

## Maintenance

The catalogue in src/wordpress/javascript/practice-catalogue.json is the sole source for these hubs and related-resource links. Add published resources and revise summaries/topics there; run `python tests/build_practice_navigation.py` before the next governed publication. Do not edit generated hub lists separately. The generated header carries the same catalogue and runtime. Source-review dates stay on the underlying resources; a navigation edit must never imply that policy guidance was re-reviewed.

## Validation

Run public boundary/provenance checks, inline JavaScript syntax checks, and the browser acceptance in tests/practice_navigation_acceptance.py. Existing visual acceptance covers desktop/tablet/mobile. The new interaction test also covers 320px, aliases, shared URL filters, empty/reset behavior, all 32 Quickstarts and keyboard focus. Final live WordPress verification remains required after Publisher execution.
