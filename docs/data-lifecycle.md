# Job data lifecycle

The fetcher briefly uses full descriptions to classify roles; it does not save
descriptions in the public job data file. After a successful source fetch,
records without a target data, AI or software category are discarded. Target
records with unknown experience or location, or an excluded status, are kept
for review but are not displayed as eligible jobs. Active, non-excluded roles
with uncertain experience or location may appear in the separate potential
matches page, with the uncertainty stated. A failed or disabled source
cannot safely reclassify old records: its existing records are preserved and
marked unknown, including older records with missing categories.

`first_seen` records the first observation retained for a source and job ID;
`last_seen` records its most recent observation. `last_checked` records the
latest successful source check. `closed_since` records the first successful
complete check that found a previously observed job absent. Further checks do
not reset that closure date. A source outage marks records unknown, not closed;
an earlier `closed_since` remains available if closure is reconfirmed. When a
posting reappears, its closure date is cleared.

Sources default to `coverage: complete`. A limited feed must declare
`coverage: partial`: an omitted record becomes unknown and is not published,
but is not treated as closed. An explicitly supplied ISO `expires_at` date
closes a partial-feed record only after that calendar date has passed; malformed
or absent dates are never guessed. An outage marks non-closed records unknown;
for partial sources an already closed record stays closed through an outage.
Invalid coverage values fail validation rather than silently treating a
partial feed as a complete one. A future partial-source connector must verify
that observed jobs are active, and must not turn a truncated response into a
successful snapshot. SmartRecruiters title-selected sources are partial. If a
previously closed job is present in the listing but its details are skipped, it
becomes unknown until fresh details are verified. Omitted unknown records are
not pruned automatically; [issue #20](https://github.com/zakariaabou/france-tech-jobs/issues/20)
tracks safe retention for these partial sources.

Closed records are removed after 180 days, measured from `closed_since`, only
after a successful source check. Active and unknown records are not aged out.
For legacy closed records without `closed_since`, the previous `last_checked`
is used as a conservative migration fallback. Missing or malformed closure
dates are never guessed and those records are retained. Because older records
may have been checked multiple times after closure, the fallback can delay
pruning. If a pruned posting later reappears, it is treated as new and its
original `first_seen` cannot be recovered from the current state file.
