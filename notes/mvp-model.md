# MVP Model

Let's sketch out this minimal-viable-product implementation and look at how it
works in action. Then we can make adjustments as appropriate.

- 30 days from detection it should expire

definitions

- a known flake -- the same failure on the same test
- a flake observation -- a test fails and makes it to main

codecov capabilities:

- for a particular branch and test, we can find the "latest test result"

# potential goals

- re-run less tests
  - don't run the known flakes (incl. 100% flakes AKA broken-in-main)
  - don't run the passing tests

# planned changes:

- add a "branches" column to `changes` table: str\[\]
- add a `head_ref` ("source branch") column to `pull` table: str\[\]

## Open Questions: "makes it to main"

- two possible definitions:

  - occurred in a SHA that is ancestor of the main branch
  - occurred in a SHA that is tip of PR branch
  - is the latest recorded test result from a PR branch (buck's)

- Should a failure from a non-tip PR revision count as a flake?

  - Our guess is no.

`merge workflow`:

```
4 -- flake? (conservatively: no, simplisitically: yes)
|\
| 3 x -- passed -- fixed?
| 2 y -- failed & passed -- flake!
|/
1
```

```
4 -- flake? yes.
|\
| 3 x -- failed & passed -- flake!
| 2 y -- failed & passed -- flake!
|/
1
```

`rebase workflow`:

```
4 C -- flake?
3 A x -- passed
2 A ~y -- failed~
1 B
```

## Future Improvements?

May never get to these.

- track "never run" tests
  - allow user to upload the full test list apart from completing the test suite
  - please let me know if suddenly my test runs stop sending this
  - can re-use this data to optimize the "waiting for test data" ingestion step

optional extensions

- we need branches if we want to extend the expiration
  - if we see a known flake but a different branch then we extend its expiry
