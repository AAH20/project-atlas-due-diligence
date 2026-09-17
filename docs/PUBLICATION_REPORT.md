# Project Atlas publication report — 2026-09-17

## Published resources
GitHub public monorepo: https://github.com/AAH20/project-atlas-due-diligence
Kaggle public dataset: https://www.kaggle.com/datasets/ahmedalaahassan/project-atlas-synthetic-m-and-a-due-diligence-vdr
Competition: https://www.kaggle.com/competitions/frontier-due-diligence-challenge-season-1

Source payload imported from commit `28c0f1fbc5ea9fe9a75c92391416af04924af5d9`, immutable release URL in Kaggle Provenance. Teaching ZIP SHA256: `5200b064ae1a7f691ef0176de60fe325fd55bb9ff37ade408354a6eff71741d8`.

## Evidence
- Public package build, validator, reference and release-check scripts completed exit 0. Release ZIP deterministic; corrupted journal rejected.
- `gh api user --jq .login` returned AAH20 with network escalation. Initial restricted-network authentication check was misleading; no credential change was needed.
- `git init -b main`, explicit standalone repository staging and commit, followed by `gh repo create AAH20/project-atlas-due-diligence --public --description ... --homepage https://www.kaggle.com/competitions/frontier-due-diligence-challenge-season-1 --source . --remote origin --push`: exit 0.
- `gh api repos/AAH20/project-atlas-due-diligence --jq '{url:.html_url,private:.private,default_branch:.default_branch}'`: public false-private, default main, expected URL.
- Corrected actual Kaggle-generated slug from the proposed `ma` spelling to `m-and-a`, regenerated and validated payload, committed and pushed; immutable corrected release used for Kaggle.
- Kaggle Link/Remote URL imported 788.28kB release. Selected Public and Other (specified in description), clicked Create; success screen explicitly confirmed dataset created. Data Explorer showed 89 extracted files and 69 columns.
- Saved dataset description with source GitHub link, competition CTA/deadline, worked-answer leakage boundaries, realism limits and full custom evaluation permission. Rendered links verified.
- Saved 80-character dataset subtitle; Settings verified Public, Save Changes disabled and Successfully saved confirmation.
- Competition public baseline guide updated with Optional Project Atlas section and both links. Rendered links plus Updated confirmation verified; no rules/rubric/required artifact changes.

## Scope and next work
Only standalone generated Project Atlas source/data/docs published. No private Scale AI/Investor OS product code, credentials, actual deal evidence or other private workflow videos. Dataset is a public teaching preview with expert realism unreviewed, not an unseen benchmark. Custom attributed research/education/evaluation permission preserves commercial rights; no participant IP assignment. Community recommendations and proposed invitation are in PARTICIPANT_OUTREACH.md. No external invitations were sent.
