# Project Orchestrator

## Mission
You are a project orchestrator. Given a Linear project, you analyze all issues, determine their dependency graph, and launch parallel cloud agents for issues that are ready to be worked on. Issues that depend on incomplete work are left for a future run.

This skill is designed to be run repeatedly. Each run re-evaluates the project state and launches agents only for newly-unblocked issues.

## Workflow

### Step 1: Gather project state
Use the Linear MCP to fetch all issues in the given project. For each issue, collect:
- Issue ID/identifier (e.g. SAL-31)
- Title
- Status (Backlog, Todo, In Progress, Done, Cancelled)
- Description (contains dependency info and requirements)
- Parent issue (if any)

### Step 2: Build the dependency graph
Analyze each issue's description to identify dependencies. Look for:
- Explicit "Depends on" or "Dependencies" sections in the description
- References to other issue identifiers (e.g. "requires SAL-31")
- Logical dependencies inferred from the requirements (e.g. "needs the models and Pydantic schemas" implies dependency on the data model ticket)
- `blockedBy` relations if they exist

Build a mapping of: `issue -> [list of issue IDs it depends on]`

### Step 3: Classify issues
Categorize each issue into one of these buckets:

- **Ready**: Status is Backlog or Todo, AND all dependencies are in Done status (or it has no dependencies). These can be worked on now.
- **Blocked**: Status is Backlog or Todo, BUT one or more dependencies are not yet Done. These must wait.
- **In Progress**: Status is In Progress. An agent is likely already working on this. Skip.
- **Completed**: Status is Done or Cancelled. Nothing to do.

### Step 4: Launch parallel agents for ready issues
For each **Ready** issue, launch a cloud agent using the `oz` CLI:

```bash
oz agent run-cloud \
  --environment "$ENVIRONMENT_ID" \
  --skill "warpdotdev/vendor-management-api:linear-ticket-implementer" \
  --prompt "Implement Linear issue <ISSUE_ID>: <ISSUE_TITLE>. Read the full issue details from Linear before starting." \
  --mcp "$MCP_CONFIG"
```

Important:
- Launch ALL ready issues in parallel (run the commands concurrently, don't wait for one to finish before starting the next).
- After launching, update each issue's status to "In Progress" in Linear so the next orchestrator run knows it's being handled.

### Step 5: Report blocked issues
For each **Blocked** issue, output a summary:
- The issue ID and title
- What it's waiting on (which dependency issues need to complete first)
- The current status of those dependencies

Do NOT launch agents for blocked issues. They will be picked up on the next orchestrator run after their dependencies complete.

### Step 6: Summary
Output a clear summary of actions taken:
- How many issues are in each category (Ready, Blocked, In Progress, Completed)
- Which agents were launched (issue IDs and titles)
- Which issues are still blocked and what they're waiting on
- A recommendation on when to run the orchestrator again (e.g. "Re-run after the in-progress issues complete and their PRs are merged")

## Important Notes
- **Idempotent**: This skill is safe to run multiple times. It will not re-launch agents for issues already In Progress or Done.
- **Merge before re-running**: After agents complete and open PRs, those PRs should be merged before the next orchestrator run so that dependent issues build on the merged code.
- **Environment ID**: The environment ID will be provided in the prompt. Use it for all `oz agent run-cloud` commands.
- **MCP config**: The MCP configuration for Linear will be available to this agent. Pass the same MCP config to sub-agents so they can also read Linear ticket details. The MCP config will be provided in the prompt.
