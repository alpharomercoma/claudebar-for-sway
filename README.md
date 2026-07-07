# ClaudeBar for Sway

![ClaudeBar for Sway](assets/claudebar.png)

A Waybar module that shows your real-time Claude Pro usage — 5-hour window percentage and time until reset — pulled directly from Anthropic's API using your existing Claude Code credentials.

---

## What it shows

```
◆ 27%  3h11m
```

- `27%` — how much of your 5-hour usage window you've consumed
- `3h11m` — time until the window resets

Hover for a tooltip that also shows your 7-day window usage.

The module is always honest about what you're looking at:

| Bar shows | Meaning |
|---|---|
| `◆ 27%  3h11m` | Live data (refreshed every 30 s; turns red at ≥ 80%) |
| `◆ 27%  3h11m` *(stale)* | Network hiccup — last known data. The countdown keeps ticking, and after 60 s without a fresh fetch the tooltip says exactly when the data was last updated. The module also carries a `stale` CSS class, unstyled by default, if you want a visual cue |
| `◆ sign in` | No account detected (signed out or credentials revoked) — you also get **one** desktop notification per session, never more |
| `◆ --` | First run, no data yet |

---

## Requirements

- [Waybar](https://github.com/Alexays/Waybar)
- [Claude Code](https://claude.ai/code) installed and signed in (`~/.claude/.credentials.json` must exist)
- Python 3 (standard library only)
- A Claude Pro or Max subscription

---

## Install

### Via dnf (Fedora)

```bash
sudo dnf copr enable alpharomercoma/claudebar
sudo dnf install claudebar
claudebar-setup
```

That's it. `claudebar-setup` wires the module into your existing Waybar config and stylesheet (backing up anything it touches), then reloads Waybar. The module appears within one 30-second poll. Updates arrive with every `dnf upgrade`.

### From a git clone

```bash
git clone https://github.com/alpharomercoma/claudebar-for-sway.git
cd claudebar-for-sway
./claudebar-setup
```

Same effect: the script is copied to `~/.config/waybar/scripts/`, your config and styles are patched (with backups), and Waybar is reloaded.

`claudebar-setup` is safe to re-run — a second invocation changes nothing. If your Waybar config is exotic (multi-bar array config, unparsable), it refuses to touch it and prints the exact snippets to add by hand instead.

### Manual setup (if you'd rather do it yourself)

<details>
<summary>Expand for the manual steps</summary>

1. Copy the script:

```bash
mkdir -p ~/.config/waybar/scripts
cp claudebar-usage ~/.config/waybar/scripts/claudebar-usage
chmod +x ~/.config/waybar/scripts/claudebar-usage
```

2. In `~/.config/waybar/config.jsonc`, add `"custom/claude"` to `modules-right`, then add the module definition:

```jsonc
"custom/claude": {
    "exec": "$HOME/.config/waybar/scripts/claudebar-usage",
    "return-type": "json",
    "interval": 30,
    "format": "{}",
    "tooltip": true
}
```

3. Append the module rules from this repo's `style.css` to your `~/.config/waybar/style.css` (the `#custom-claude` blocks, including `.idle`, `.critical`, and `.signin`).

4. Reload Waybar:

```bash
pkill -SIGUSR2 waybar
```

</details>

---

## How it works

The script reads your OAuth credentials from `~/.claude/.credentials.json` (written by Claude Code when you sign in). If the access token is expired or within 5 minutes of expiring, the script refreshes it itself — using the `refreshToken` in that file against Anthropic's OAuth token endpoint, then writing the rotated tokens back atomically — exactly as Claude Code does on startup. This means the bar stays accurate on its own, without you ever having to launch a `claude` session. It then calls:

```
GET https://api.anthropic.com/api/oauth/usage
Authorization: Bearer <token>
anthropic-beta: oauth-2025-04-20
```

The response contains `five_hour.utilization` (the percentage) and `five_hour.resets_at` (the reset timestamp).

**Freshness.** Every successful fetch caches the raw values (`~/.cache/claudebar-usage.json`), including the reset timestamp and the fetch time. If a poll fails (offline, rate-limited, API down), the bar serves the cache — but the countdown is recomputed on every render so it keeps ticking, and after 60 seconds without a successful fetch the tooltip tells you exactly how old the data is. The module keeps its normal color; a `stale` CSS class is emitted alongside `active`/`critical` if you'd like to style staleness yourself. You can always trust what you see.

**Sign-in detection.** Credential problems (missing file, revoked refresh token) are distinguished from network problems. When you're genuinely signed out, the bar shows `◆ sign in` and sends a single desktop notification per login session — it never nags. Once you sign in again, everything recovers automatically within one poll.

---

## Removing

```bash
sudo dnf remove claudebar   # rpm installs
```

Then, in either install mode: remove `"custom/claude"` from `modules-right` and the `"custom/claude"` block from your Waybar config, delete the `#custom-claude` rules from your `style.css`, and (git installs) delete `~/.config/waybar/scripts/claudebar-usage`.

---

## Sway integration note

Fedora Sway loads bar configuration from `/usr/share/sway/config.d/` and `/etc/sway/config.d/` via a layered include system. Your user config in `~/.config/sway/config.d/` takes precedence. **Do not edit files under `/etc/sway/` or `/usr/share/sway/` directly** — override them by placing a file with the same name under `~/.config/sway/config.d/`.

Waybar is launched separately from Sway's built-in bar. The default Fedora config in `/etc/sway/config.d/` (typically `90-bar.conf`) starts Waybar automatically. If you need to disable the default bar to avoid conflicts, create an empty override:

```bash
echo -n > ~/.config/sway/config.d/90-bar.conf
```

Then start Waybar yourself via `exec waybar` in your sway config or a separate autostart file.

---

## Troubleshooting

**Module shows `◆ sign in`**
No usable Claude Code account was found — the credentials file is missing, unreadable, or its refresh token was revoked (e.g. you signed out). Run `claude` once to re-authenticate; the bar recovers within one 30-second poll.

**Tooltip says the data is stale**
The last poll(s) failed — usually a network hiccup or a transient API error. Nothing to do; it recovers on the next successful poll. The tooltip shows how old the displayed data is.

**Module shows `◆ --`**
No cached data yet and the API call failed. Check your connection, then run the script directly to see what's happening:
```bash
~/.config/waybar/scripts/claudebar-usage    # git installs
claudebar-usage                              # rpm installs
```

**Waybar not picking up changes**
```bash
pkill -SIGUSR2 waybar
```
If that doesn't work, kill and restart it:
```bash
pkill waybar && waybar &
```

---

## CodexBar

Also want your Codex (ChatGPT) usage next to this? See the companion module: [CodexBar for Sway](https://github.com/alpharomercoma/codexbar-for-sway). Both setup tools compose cleanly in the same Waybar config.

---

## License

MIT — see [LICENSE](LICENSE).
