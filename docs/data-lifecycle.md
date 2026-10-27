# Job data lifecycle

The fetcher briefly uses full descriptions to classify roles; it does not save
descriptions in the public job data file. After a successful source fetch,
records without a target data, AI or software category are discarded. Target
records with unknown experience or location, or an excluded status, are kept
for review but are not displayed as eligible jobs. A failed or disabled source
cannot safely reclassify old records: its existing records are preserved and
marked unknown, including older records with missing categories.

`first_seen` records the first observation retained for a source and job ID;
`last_seen` records its most recent observation. `last_checked` records the
latest successful source check. `closed_since` records the first successful
complete check that found a previously observed job absent. Further checks do
not reset that closure date. A source outage marks records unknown, not closed;
an earlier `closed_since` remains available if closure is reconfirmed. When a
posting reappears, its closure date is cleared.

Closed records are removed after 180 days, measured from `closed_since`, only
after a successful source check. Active and unknown records are not aged out.
For legacy closed records without `closed_since`, the previous `last_checked`
is used as a conservative migration fallback. Missing or malformed closure
dates are never guessed and those records are retained. Because older records
may have been checked multiple times after closure, the fallback can delay
pruning. If a pruned posting later reappears, it is treated as new and its
original `first_seen` cannot be recovered from the current state file.
