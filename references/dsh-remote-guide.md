# How dsh-remote works in Tools-SPACE

Tools-SPACE runs in a remote workspace, but DeepSeek Harness Desktop and its agent session stay on the machine running DSH. The third-party [`dsh-remote`](dsh-remote/README.en.md) plugin connects that session to the SSH host. This reference uses plugin **1.4.1**, matching the installed bundle inspected on DSH Desktop **0.2.2-rc.5**. The [submodule](dsh-remote) pins upstream tag `v1.4.1` (`aafdcf4a7f530a226bbf8228f6a5affd26fe7014`). It is reference material, not a Tools-SPACE plugin installation.

## One workspace, two paths

```text
DSH Desktop / agent (local)
  Session cwd: $DSH_HOME/remote-workspaces/<host-user-port>/Tools-SPACE
  Local mirror: a real local folder, not an SSH mount
        │ workspace binding = SSH machine + remote root
        ├─ rw_exec                  → SSH command on the remote host
        ├─ rw_read_file / rw_edit   → live remote files over SFTP
        └─ rw_sync / rw_push        ⇄ copies between the two folders
  Remote root: <remote-root>/Tools-SPACE
```

A saved machine gives the plugin connection settings; on its own it does not turn an existing local session into a remote one. Choosing a remote folder from **Add workspace** creates or reuses its local mirror and opens the workspace in DSH. For tool-driven setup, use `rw_connect` and `rw_pick_workspace`, then open a session rooted at the mirror if starting from a local session. The plugin resolves the remote machine and folder from the session's workspace binding, so separate sessions can work on different hosts. See [workspace setup in the upstream reference](dsh-remote/docs/reference.en.md#L153-L160) and the [binding implementation](dsh-remote/lib/binding.js).

## Which operation goes where?

| To do this | Use this | Where it acts |
| --- | --- | --- |
| Check which workspace the session is bound to | `rw_info` | Shows the remote root and local mirror, and runs a short SSH command to check reachability. |
| Browse, read, or search current project files | `rw_list_dir`, `rw_read_file`, `rw_search`, or the remote Files pane | The live remote tree; no mirror sync needed. |
| Save a change to the shared project | `rw_edit` or `rw_write_file` | The live remote file; no `rw_push` needed. |
| Run Git, a build, or tests | `rw_exec` | The remote shell, starting at the remote workspace root by default. |
| Inspect or process a local copy | `rw_download` for one file, or `rw_sync` for the workspace | Copies files to the local mirror. A normal local shell still runs locally. |
| Send changes back after working on local copies | `rw_upload` for an explicit file transfer, or `rw_push` for the workspace | Copies local content to the remote host. |

The mirror is **not** automatically kept equal to the remote tree. `rw_sync` pulls and `rw_push` sends workspace changes; both are bounded and check for conflicts when both copies changed. Use `dryRun: true` to inspect the plan before a bulk transfer. Automatic push is optional and off by default. In this Tools-SPACE session, native write/edit mutations are refused; use the remote tools to save project changes. For a local artifact, transfer it explicitly and verify it with `rw_stat` or `rw_read_file` before saying it is saved remotely. The plugin's [remote sandbox](dsh-remote/docs/reference.en.md#L349) is a containment guard, not a substitute for permissions on the SSH host.

## See it in this session

Run `rw_info`, then `rw_exec` with `pwd; git status --short`. The `pwd` from `rw_exec` shows the **remote** repository; the CWD printed in the session context is the **local** mirror. If `rw_info` shows `Connected: no` alongside `Ping: OK`, those lines measure different things: the first looks for a persistent client before the second runs its SSH check. See the [`rw_info` implementation](dsh-remote/lib/main.js#L2194-L2237).

For an example that writes a file, use `rw_edit` on the remote file, then verify it with `rw_read_file` and inspect the repository diff with `rw_exec`. There is no local-to-remote copy step in that loop.

## Where to read the implementation

- [Bundle patch](dsh-remote/cordis.patch.yml) and [boot entry](dsh-remote/lib/boot.js): how the profile loads the plugin.
- [Main plugin](dsh-remote/lib/main.js), [workspace binding](dsh-remote/lib/binding.js), and [SSH pool](dsh-remote/lib/pool.js): how an `rw_*` call finds the right host and folder.
- [Remote file operations](dsh-remote/lib/remote-fs.js), [workspace file browser adapter](dsh-remote/lib/workspace-files-remote.js), and [mirror transfer logic](dsh-remote/lib/sync.js): how live I/O differs from copying files.
- [Upstream reference](dsh-remote/docs/reference.en.md) and [troubleshooting](dsh-remote/docs/troubleshooting.en.md): settings, tool behaviors, and connection issues.
