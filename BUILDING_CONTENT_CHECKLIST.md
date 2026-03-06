# Building-by-Building Content Checklist

Use this for each property folder so every image is accounted for.

## Workflow (repeat for each building)

1. Pick one building folder.
2. Run:
   - `python3 scripts/media_audit.py --building "<building folder name>"`
3. Add missing photos to `index.html` (`data-gallery` or a new card).
4. Re-run the audit for that building.
5. Mark complete only when:
   - Unused files are `0`, or
   - remaining files are intentionally excluded and documented below.

## Building Tracker

- [ ] `7455 Union Park Ave`
- [ ] `hotel in nephi utah under construction`
- [ ] `MDH Development LLC` (shared portfolio folder; process by project sections)
- [ ] `Pleasant-Grove-Sale-Flyer.pdf` (extract images and include where needed)
- [ ] `Ephraim-Retail-Flyer.pdf` (extract images and include where needed)

## Intentional Exclusions Log

Use this section if a file should stay unused (duplicate, low quality, etc.).

- `path/to/file.ext` - reason

