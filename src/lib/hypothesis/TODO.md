goals:

- test expiration -- flakiness expires after 30 passes
- tests can fail with some liklihood
  - measure the likelihood of flake-then-fix in a pr yielding false positives
- implement some of the planned improvements to give us cost estimates
- PR behavior: merge, rebase, squash

definitions:

- false positive -- labelled as flake, when it's actually not -- this breaks
  prod!
- false negative -- labelled as failure, when it's just flaky -- status quo.
