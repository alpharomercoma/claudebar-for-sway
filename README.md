# ClaudeBar for Sway

A Waybar module that shows your real-time Claude Pro usage — 5-hour window percentage and time until reset — pulled directly from Anthropic's API using your existing Claude Code credentials.

**Developer:** Alpha Romer Coma

---

## What it shows

```
◆ 27%  3h11m
```

- `27%` — how much of your 5-hour usage window you've consumed
- `3h11m` — time until the window resets

Hover for a tooltip that also shows your 7-day window usage.

---

## Requirements

- [Waybar](https://github.com/Alexays/Waybar)
- [Claude Code](https://claude.ai/code) installed and signed in (`~/.claude/.credentials.json` must exist)
- Python 3 (standard library only)
- A Claude Pro or Max subscription

---

## Setup

### 1. Copy the script

```bash
mkdir -p ~/.config/waybar/scripts
cp claude-usage ~/.config/waybar/scripts/claude-usage
chmod +x ~/.config/waybar/scripts/claude-usage
```

### 2. Add the module to your Waybar config

In `~/.config/waybar/config.jsonc`, add `"custom/claude"` to `modules-right` where you want it to appear, then add the module definition:

```jsonc
"modules-right": [
    "idle_inhibitor",
    "custom/claude",
    "pulseaudio",
    // ... rest of your modules
],

"custom/claude": {
    "exec": "$HOME/.config/waybar/scripts/claude-usage",
    "return-type": "json",
    "interval": 30,
    "format": "{}",
    "tooltip": true
}
```

If you don't have a `~/.config/waybar/config.jsonc` yet, copy the provided `config.jsonc` from this repo — it's based on the Fedora Sway default and has the module already placed left of the volume control.

### 3. Add the styles

Append the contents of `style.css` to your `~/.config/waybar/style.css`, or copy it wholesale if you don't have one yet.

The relevant section:

```css
#custom-claude {
    padding: 0 10px;
    background-color: #2b303b;
    color: #d97757;
    border-left: 2px solid #d97757;
}

#custom-claude.idle {
    color: #666e7a;
    border-left-color: #666e7a;
}

#custom-claude.critical {
    color: #eb4d4b;
    border-left-color: #eb4d4b;
}
```

### 4. Reload Waybar

```bash
pkill -SIGUSR2 waybar
```

---

## How it works

The script reads your OAuth access token from `~/.claude/.credentials.json` (written by Claude Code when you sign in) and calls:

```
GET https://api.anthropic.com/api/oauth/usage
Authorization: Bearer <token>
anthropic-beta: oauth-2025-04-20
```

The response contains `five_hour.utilization` (the percentage) and `five_hour.resets_at` (the reset timestamp). On network failure, the last successful result is served from `~/.cache/claudebar-usage.json` so the bar never flashes an error for a transient hiccup.

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

**Module shows `◆ --`**
The script has no cached data yet and the API call failed. Check that `~/.claude/.credentials.json` exists and that you're connected to the internet. Run the script directly to see the error:
```bash
python3 ~/.config/waybar/scripts/claude-usage
```

**Token expired**
Claude Code refreshes the token automatically when you run it. Start a Claude Code session and the token in `~/.claude/.credentials.json` will be updated. The bar will recover on the next 30-second poll.

**Waybar not picking up changes**
```bash
pkill -SIGUSR2 waybar
```
If that doesn't work, kill and restart it:
```bash
pkill waybar && waybar &
```
