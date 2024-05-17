# Milestones

## M0 "What Datadog does"

- a test report is "main branch" iff SHA appears on main history
  - only merge workflows have full support, this way
- all errors are equal -- AssertionError is the same as FileDoesNotExistError
- flakes are "fixed" after not-failing for 30 days

## M? "Better expiry"

- why:

  - flakes that run rarely will be falsely "fixed" this for example, this is
    still flaky even if the last report was 8 mos ago.
    ```
    __*__*____*_*_*
    ```
  - flakes that run often will be marked "fixed" much too late e.g. this test is
    fixed, even if the test reports came in 1s apart:
    ```
    ____*__*_*___*__*__*___________________________________________
    ```

- how:

  - M0?: don't use timestamps, just use "report index" -- one per report
    - flakes are "fixed" after _passing_ for 30 runs
    - joe: under M0, we might be able to do this "for free"
  - M1?: even better: use flake percentage to determine the passes-till-fixed
    param
    - e.g a 100% flake might be fixed after 10 passes
    - this is approximates what an expert would do pretty well
    - a 1% flake might be fixed after 1000 passes
    - cost estimate: we'd need to start tracking flake-percentage for each
      flake, would need a new table

## M? "errors matter"

- why:

  -

- how:

  - store error messages
  - compare error messages
    - "failure normalization"
      - use a series of regexes to replace "2024-11-11" with "$DATE"
      - reasonable defaults
      - user-configurable list of regex/replacement pairs
    - "by error type" AssertionError is different from KeyError

## M? "rebase workflows"

- test results from SHAs that are rebased/squashed during merge are thrown away
- we need to know which SHAs were rebased/squashed to main
  - we already do this for merge commits, for sure
  - rebase?
  - squash?

## M? "PR authors fix flakes"

- only a failure/flake from prior revisions of a PR should be discounted
