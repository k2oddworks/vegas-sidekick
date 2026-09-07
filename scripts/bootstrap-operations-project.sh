#!/usr/bin/env bash
set -euo pipefail

# Creates/links the Vegas Sidekick Operations GitHub Project and adds the exact
# operating-stage field. Requires GitHub CLI auth with the `project` scope:
#   gh auth refresh -s project

TITLE='Vegas Sidekick Operations'
OWNER="${GH_PROJECT_OWNER:-$(gh api user --jq .login)}"
REPO_NAME="${GH_REPO_NAME:-$(gh repo view --json name --jq .name)}"

project_number=$(gh project list --owner "$OWNER" --format json --jq ".projects[] | select(.title == \"$TITLE\") | .number" | head -1)
if [[ -z "$project_number" ]]; then
  project_number=$(gh project create --owner "$OWNER" --title "$TITLE" --format json --jq '.number')
  echo "Created project #$project_number"
else
  echo "Using existing project #$project_number"
fi

gh project link "$project_number" --owner "$OWNER" --repo "$REPO_NAME" 2>/dev/null || true

if ! gh project field-list "$project_number" --owner "$OWNER" --format json --jq '.fields[].name' | grep -Fxq 'Operations Stage'; then
  gh project field-create "$project_number" \
    --owner "$OWNER" \
    --name 'Operations Stage' \
    --data-type SINGLE_SELECT \
    --single-select-options 'Inbox,P0 Accuracy,P1 Revenue,P2 Growth,P3 Enhancement,In Progress,Needs Kris,Ready to Ship,Shipped / Verify,Done' >/dev/null
  echo 'Created Operations Stage field.'
else
  echo 'Operations Stage field already exists.'
fi

if ! gh project field-list "$project_number" --owner "$OWNER" --format json --jq '.fields[].name' | grep -Fxq 'Maintenance Debt'; then
  gh project field-create "$project_number" --owner "$OWNER" --name 'Maintenance Debt' --data-type NUMBER >/dev/null
  echo 'Created Maintenance Debt field.'
fi

if ! gh project field-list "$project_number" --owner "$OWNER" --format json --jq '.fields[].name' | grep -Fxq 'Content Score'; then
  gh project field-create "$project_number" --owner "$OWNER" --name 'Content Score' --data-type NUMBER >/dev/null
  echo 'Created Content Score field.'
fi

echo
echo "Project ready: $TITLE (#$project_number)"
echo "In the GitHub UI, make the primary Board view group by 'Operations Stage'."
