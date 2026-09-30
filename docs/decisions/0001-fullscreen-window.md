# 0001: Use `fullscreen_window()` instead of `--start-fullscreen`

- **Status:** Accepted. Fullscreen vs. maximize is still open; see [Options considered](#options-considered).
- **Date:** 2026-09-30
- **Tested on:** macOS 26.5.2, Chrome 154.0.8037.58, ChromeDriver 154.0.8037.92, 1728×1117 display

## Context

`DriverFactory.get_driver()` should give every test a browser that fills the screen, headed or headless.

The first version passed Chrome's `--start-fullscreen` flag. Headless runs were fine, but headed runs (`pytest -H`) on macOS usually opened at Chrome's default 1200×950 window.

### Why `--start-fullscreen` fails on macOS

It depends on which app has focus when Chrome launches. Chrome requests fullscreen at the end of startup ([`MaybeToggleFullscreen` in `startup_browser_creator_impl.cc`](https://github.com/chromium/chromium/blob/main/chrome/browser/ui/startup/startup_browser_creator_impl.cc)). That's the same code on every platform, so macOS isn't excluded. But when another app, like Terminal, still has focus at that moment, macOS drops the request. When you run `pytest -H` from a terminal, the terminal has focus, so this is the normal case, not an edge case.

Measured, with the frontmost app checked just before each launch:

| Focused app before launch | `--start-fullscreen` went fullscreen |
|---|---|
| Terminal | 1 of 5 |
| Finder | 4 of 4 |

The focus explanation comes from this pattern. We didn't find Chrome or macOS documentation that confirms it.

There's a second problem. Even when the flag works, the window shrinks from 1084 to 996 pixels tall within half a second, while Chrome still reports it as fullscreen. We don't know why.

### Headless has no real screen

Headless Chrome pretends the screen is 800×600, so "fullscreen" alone gives an 800×600 window. `--screen-info={1920x1080}` gives headless Chrome a 1920×1080 virtual screen to fill. `--window-size=1920,1080` doesn't work: going fullscreen shrinks the window back to the 800×600 screen.

## Options considered

All headed runs below had Terminal focused before launch. Headless runs used `--screen-info={1920x1080}`.

| Option | Kind | Headed result | Headed window | Headless viewport |
|---|---|---|---|---|
| `--start-fullscreen` | Chrome flag | 1 of 5 fullscreen | 1200×950 when it fails | 1920×1024 |
| `fullscreen_window()` | WebDriver method | 10 of 10 fullscreen\* | 1728×1084 | 1920×1024 |
| `--start-maximized` | Chrome flag | 3 of 3 maximized | 1728×994 | 1920×937 |
| `maximize_window()` | WebDriver method | 3 of 3 maximized | 1728×994 | 1920×937 |

\* 5 of these runs had Terminal focused and 5 had Finder focused. It never shrank.

- **Fullscreen** hides the macOS menu bar and Dock, and in headless mode Chrome's toolbar too, so pages get the most room.
- **Maximized** fills the screen but keeps the menu bar, Dock, and Chrome's toolbar visible.
- A **WebDriver method** is sent to the already-running browser, and ChromeDriver waits until the window has changed before returning. A **Chrome flag** is handled during Chrome's own startup, which is where the focus race happens.

## Decision

Keep `--screen-info={1920x1080}` for headless. Drop `--start-fullscreen`, and call `driver.fullscreen_window()` right after the driver is created, inside `get_driver()` before it's returned.

- It goes in `get_driver()` so every driver gets it, whether it comes from the `driver` fixture or a direct call.
- It runs before the first navigation, so pages load at full size from the start.

## Consequences

- Headed runs are reliably fullscreen on macOS, whichever app has focus.
- Setting up the window is now a WebDriver call after launch, not a launch option.
- If fullscreen is ever swapped for maximize, either maximize option is reliable. `--start-maximized` doesn't have the focus race, so maximize could stay a startup flag.
- If `--start-fullscreen` is ever reconsidered, retest headed runs with a terminal focused. That's the case that fails.
