A flake_period table with four columns:

- test name
- normalized error
- start: timestamp
- last_seen: timestamp
- fail: int
- run: int
- end (nullable)

```
________*______________*___________*_______________*____________*____________X
____AAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAABBBBBBBBBBBABBBBBBBBBBBBBBBBBB

A: S-----------------------------------E-----------E   "timeout"
B:                          S-----------------------------------------E "connection lost"
C: "assertion error"


________*___
        S---

________*________*___
        S--------s---



________*________*_____*_____
        S--------------s-----

________*________*_____________...______________________*
        S--------E                                      E

```
