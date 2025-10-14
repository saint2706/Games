# GitHub Actions Event Payloads

This directory contains sample event payloads for testing GitHub Actions workflows locally with `act`.

## Available Event Files

### push.json

Use this for workflows triggered by push events:

```bash
./scripts/run_workflow.sh ci --event .github/workflows/events/push.json
```

This simulates a push to the master branch.

### pull_request.json

Use this for workflows triggered by pull request events:

```bash
./scripts/run_workflow.sh ci --event .github/workflows/events/pull_request.json
```

This simulates opening a pull request.

### workflow_dispatch.json

Use this for manually-triggered workflows with inputs:

```bash
./scripts/run_workflow.sh test --event .github/workflows/events/workflow_dispatch.json
```

This simulates manually running a workflow with specific input parameters.

### release.json

Use this for workflows triggered by release events:

```bash
./scripts/run_workflow.sh publish --event .github/workflows/events/release.json
```

This simulates publishing a release tagged as `v1.0.0`.

## Customizing Event Payloads

You can create your own event files based on these examples:

1. Copy an existing event file:

   ```bash
   cp .github/workflows/events/push.json .github/workflows/events/my-push.json
   ```

1. Modify the JSON to match your test scenario

1. Use it with act:

   ```bash
   ./scripts/run_workflow.sh ci --event .github/workflows/events/my-push.json
   ```

## Event Payload Structure

Each event type has a different structure. For full documentation, see:

- [GitHub Webhook Events](https://docs.github.com/en/developers/webhooks-and-events/webhooks/webhook-events-and-payloads)
- [GitHub Actions Events](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)

## Common Modifications

### Change Branch

In `push.json` or `pull_request.json`, modify the `ref` field:

```json
"ref": "refs/heads/feature-branch"
```

### Change Workflow Inputs

In `workflow_dispatch.json`, modify the `inputs` object:

```json
"inputs": {
  "python-version": "3.11",
  "marker": "not slow",
  "collect-coverage": true
}
```

### Add Repository Information

All event files should include repository information:

```json
"repository": {
  "name": "Games",
  "full_name": "saint2706/Games",
  "owner": {
    "login": "saint2706"
  }
}
```

## Tips

- Keep your custom event files in this directory for consistency
- Use descriptive filenames: `push-hotfix.json`, `pr-from-fork.json`, etc.
- Test with different event types to ensure workflow flexibility
- Refer to actual GitHub webhook payloads in the Actions UI for accuracy

## Related Documentation

- [Running Workflows Locally](../../../docs/development/LOCAL_WORKFLOWS.md)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
