# Hub database — stage 2.5.1

The migration is stored under scripts/ (excluded from public static assets by .assetsignore). Apply once to the dedicated vegas-sidekick-hub D1 database using its migration mechanism or console; do not apply to another database. No production data is included.

The database contains projects, tasks, recurrence rules and append-only activity. IDs are server-generated UUIDs. Dates use YYYY-MM-DD in Las Vegas local calendar time; timestamps use UTC. Department codes correspond to the eight agreed departments. Archive records instead of deleting them. The API must validate dates, identifiers, title lengths, actor identity and authorization, set updated_at and revision on every mutation, use optimistic concurrency, and atomically append activity with each mutation (including completion and reopening). Completion clears current completion fields when reopened but historical events preserve prior completion. Recurrence scheduling, skip events, prioritization, verification and search are future API/workflow work; schema alone does not execute them. No credentials or private task data belong in GitHub. No production migration or Worker change is implied by this commit.

Before enabling private writes, verify legacy credential revocation, API token checks, alternate endpoints, and authentication/authorization for each route.
