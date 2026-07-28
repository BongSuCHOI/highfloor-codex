# Releasing Highfloor

This is the maintainer checklist for a tagged Highfloor release. It keeps
versioning, distribution behavior, documentation, and mixed-license
provenance in one place so they do not have to be reconstructed from the
README or `AGENTS.md`.

## Release boundary

A release publishes a reviewed repository state and the exact skills and
agents named in the two manifests. It does not publish a plugin or a finished
agent harness unless a future release explicitly adds and versions that
distribution surface.

Treat these as public interfaces:

- skill directory names, frontmatter names, and runtime contracts;
- agent filenames, names, roles, and authority;
- installer destinations, ownership, update, backup, and uninstall behavior;
- license and provenance boundaries;
- documented commands and compatibility claims.

## 1. Choose the version

Use Semantic Versioning from the first public tag:

- **patch** for compatible fixes, documentation corrections, and internal
  validation improvements;
- **minor** for compatible capabilities, new skills or agents, and additive
  installer behavior;
- **major** for incompatible names, runtime contracts, installer ownership,
  destinations, migration behavior, or license boundaries.

Before changing `VERSION`, decide whether users of the previous tag can update
without changing their configuration or workflow. If not, document the
migration and choose the corresponding version.

## 2. Close the changelog

1. Move the release's entries out of `## [Unreleased]`.
2. Add `## [X.Y.Z] - YYYY-MM-DD`.
3. Leave a new empty `## [Unreleased]` section above it.
4. Update `VERSION` to `X.Y.Z`.
5. Update pinned tag examples and release-status text in `README.md`,
   `README_KR.md`, and `docs/INSTALLATION.md`.

Write notes for users: changed behavior, compatibility, migration, recovery,
and known limits. Do not turn internal implementation details into release
notes unless they affect those users.

## 3. Audit distribution and licensing

For every added, copied, adapted, or substantially rewritten component:

1. classify it as original, independently worded from a method, modified
   derivative, retained upstream file, or runtime-only dependency;
2. record the exact upstream project and version or commit when known;
3. record the upstream license and bundle its text when redistribution
   requires it;
4. add a prominent modification notice for derivatives;
5. update the skill's `references/upstream*.md`,
   `skills/CX_MIGRATION_MANIFEST.md`, and `THIRD_PARTY_NOTICES.md`;
6. confirm that the root MIT license is not described as relicensing
   third-party or derivative material.

Do not release new material with unresolved provenance. Entries under
Sustainable Use License 1.0 must retain that license and its distribution
conditions. If a release changes which license governs a public interface,
treat that as a major compatibility decision and explain it prominently.

## 4. Check installer migration

Review both manifests and answer:

- Which names will be installed or replaced?
- Which names were present in the previous release but are now retired?
- Will update back up and remove those retired entries?
- Are unrelated user entries still untouched?
- Does a destination or state-format change require an explicit migration?

For a removed or renamed item, add migration and recovery notes. Do not rely
on users editing a manifest: the published manifest defines what Highfloor
owns, and removing a previously managed name retires that installed entry.

## 5. Run the release checks

From the repository root:

```sh
./scripts/validate.sh
./scripts/test-install.sh
```

`validate.sh` includes the release consistency check. It verifies the current
SemVer, dated changelog entry, pinned version examples, required release
files, catalog coverage, and per-skill provenance records. The installer test
exercises install, update, backup, doctor, uninstall, explicit destinations,
and default `CODEX_HOME` destinations.

If a required external host behavior cannot be observed, record it as
`NOT_PROVEN`; do not convert a local file check into a host compatibility
claim.

## 6. Review the candidate

Review the complete release diff, not only the final version bump. Confirm:

- README English and Korean descriptions are semantically aligned;
- `CHANGELOG.md` describes all user-visible changes;
- names and counts match the manifests;
- installer and security documentation match current behavior;
- no secrets, local absolute paths, caches, session logs, or temporary assets
  are included;
- the selected README banner and local links resolve;
- CI passes on the exact commit to be tagged.

Use specialist review only where the release changed that boundary. For
example, request security review for trust-boundary changes and licensing
review for new third-party material; do not run every reviewer for every
release.

## 7. Tag and publish

After the candidate commit is reviewed and CI is green:

```sh
git tag -s vX.Y.Z -m "Highfloor vX.Y.Z"
git push origin vX.Y.Z
```

If signed tags are not available, use an annotated tag and disclose the
project's signing policy. Create the GitHub release from the tag, copy the
user-facing changelog entry, and include migration or recovery instructions.

Do not retag a published version. Correct it with a new patch release.

## 8. Verify the published artifact

Test the immutable tag, not `main`:

```sh
curl -fsSL https://raw.githubusercontent.com/BongSuCHOI/highfloor-codex/vX.Y.Z/install.sh \
  | HIGHFLOOR_REF=vX.Y.Z sh -s -- update --dry-run
```

Confirm that the GitHub release, source archive, raw installer URL, changelog,
and `VERSION` all identify the same version. If publication is incomplete,
document the issue before directing users to the release.

## Emergency correction

For a broken release:

1. stop recommending the affected tag;
2. describe impact and safe recovery;
3. fix on a new version;
4. run the complete release checks;
5. publish a patch release;
6. keep the original tag and changelog history intact.
