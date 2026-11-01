# G595 D1 successor frame candidate — INACTIVE

Owner source approval: https://github.com/sonvhse06072/personal-coding-platform/issues/595#issuecomment-6552078840
Candidate parent: b19e25fb35dbc94c8d725849943453aabb667e86. This revision prepares
neutral QA; it is not an approved/active ProjectBaseline or a sealed trial seed.
Preserve PROJECT-BASELINE.md, composer.lock and all old benchmark refs/PRs.

## Purpose and scope

Prepare equal, independent real Drupal Unit/Kernel/PHPCS environments for fresh
G595-D1. The accepted contract is in PCP's 2026-11-01-benchmark595-contracts.json,
acceptance SHA256 2cd5b1f7ff52414457216d87f8e6d6b3ef5be06df03b0c59e240903b6108d1ce.
Do not implement CapacityAvailability or its acceptance tests during setup.
No old T01/F2/T02 task, solution or denied egress is reused. No real application data.

## Neutral quality policy

Both future delivery bases benchmark/595-d1-direct and benchmark/595-d1-pcp
must begin at the SAME independently accepted, post-QA successor source. They are
not created by this PR. Both arms run Composer validate, PHP syntax, Drupal PHPCS,
and actual nonempty Drupal Unit and Kernel suites, failing skipped/incomplete/risky
or empty suites. Current baseline tests exercise only the original fixture; their
PASS does not establish future D1 acceptance. Acceptance tests belong to future
independent implementations, after the source/frame decision.

Hosted validation checks the actual PR head, not its synthetic merge ref. Manual
validation requires an exact candidate SHA; checkout HEAD and lock bytes are proven.
PHP8.4 and MariaDB11.8 align local example and hosted profiles. Patch versions and
image digests remain observed physical provenance, not asserted from major pins.
Equivalent independent review and accepted-head CI remain mandatory for both arms.
No browser/F1/R1 dependencies or reporter changes in this scope.

## Isolation and authority

The DDEV example has no active topology: comments plus override_config:false only.
Do not copy its placeholders into live config. A separately authorized operator must
prepare private per-arm workspace/database/cache/network, bound resources, prestarted
web/db and read-only private per-job manifests/lease/token state. Developer receives
only the fixed-phase capability, never Docker/Runtime/Router/Executor/GitHub or host
credentials. No implicit DDEV start/name rewrite is authorized by this source PR.
No site, worker, build/pull, activation, login, model, trial, merge or deployment here.

## Budget, chronology and adoption

Use the existing PCP adaptive/anomaly policy; counters are durable and never reset.
Report executable approval/slot release through independent accepted PR, all roles'
usage, test/repair attempts and timed Owner attention with unknown values null.
No benchmark records or latency quantiles arise from neutral CI.
After independent source review/merge and genuine postmerge CI, seal the actual
successor source in a NEW baseline/acceptance revision. Never silently rewrite the
original b19 contract or an approved revision. Exact physical resources, provider/
CLI/toolchain parity, credential/egress, daemon residual-risk and ONE-pair execution
selection remain separate decisions. #595 stays HOLD/NOT GO.
Rollback rejects these inactive candidates; retain historical assets and evidence.
