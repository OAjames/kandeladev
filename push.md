<!--
push.md

Purpose:
Provide a concise, practical reference for using "git push" to publish commits and tags from a local repository to a remote. Covers common workflows, important flags, safe practices, common issues, and ready-to-copy commands.

Sections:
- Overview
  - What "git push" does and when to use it.
- Common commands & short explanations
  - git push
  - git push origin <branch>
  - git push -u origin <branch> (set upstream)
  - git push --tags
  - git push --all
  - git push --delete origin <branch>
  - git push --force vs --force-with-lease
- Examples (copy-paste friendly)
  - Initial repository: git push -u origin main
  - Regular push: git push
  - After rebase: git push --force-with-lease
  - Push a tag: git push origin v1.2.3
  - Delete remote branch: git push origin --delete feature/foo
- Flags & semantics
  - -u/--set-upstream: create tracking relationship for future pushes/pulls
  - --force: overwrite remote branch (destructive)
  - --force-with-lease: safer alternative to --force
  - --tags: push all tags
  - --follow-tags: push annotated tags reachable from refs
- Best practices & safety
  - Prefer --force-with-lease over --force
  - Pull/rebase and resolve conflicts locally before pushing
  - Avoid pushing large files; use Git LFS for large assets
  - Communicate with team before rewriting shared history
- Troubleshooting
  - "non-fast-forward" / rejected push: pull + rebase or use --force-with-lease after confirming
  - Authentication failures: check credentials, token scopes, and remote URL
  - Large objects rejected: use Git LFS or remove large files from history
- Related topics and references
  - git fetch, git pull, git rebase, git remote, git branch, Git LFS
  - Official git docs: https://git-scm.com/docs/git-push
- Metadata
  - Audience: Developers with basic Git knowledge
  - Prerequisites: Local commits to push, configured remote (origin)
  - Last updated: [24/11/2025]
  - Author: [@Olakunle_James]
-->