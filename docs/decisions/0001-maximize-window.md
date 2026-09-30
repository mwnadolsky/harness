# 0001: Maximize the browser window with `maximize_window()`

- **Status:** Accepted
- **Date:** 2026-09-30
- **Tested on:** macOS 26.5.2, Chrome 154.0.8037.58, ChromeDriver 154.0.8037.92, 1728×1117 display

## Context

`DriverFactory.get_driver()` should give every test a browser that fills the screen, headed or headless.

The first version passed Chrome's `--start-fullscreen` flag. Headless runs were fine, but headed runs (`pytest -H`) on macOS usually opened at Chrome's default 1200×950 window. Fixing that turned up a second, bigger problem with fullscreen itself.

### Problem 1: `--start-fullscreen` fails when another app has focus

Chrome requests fullscreen at the end of startup ([`MaybeToggleFullscreen` in `startup_browser_creator_impl.cc`](https://github.com/chromium/chromium/blob/main/chrome/browser/ui/startup/startup_browser_creator_impl.cc)). That's the same code on every platform, so macOS isn't excluded. But when another app, like Terminal, still has focus at that moment, macOS drops the request. When you run `pytest -H` from a terminal, the terminal has focus, so this is the normal case.

| Focused app before launch | `--start-fullscreen` went fullscreen |
|---|---|
| Terminal | 1 of 5 |
| Finder | 4 of 4 |

The focus explanation comes from this pattern. We didn't find Chrome or macOS documentation that confirms it. Even when the flag worked, the window shrank from 1084 to 996 pixels tall within half a second, for unknown reasons.

`driver.fullscreen_window()`, a WebDriver command sent after launch, doesn't have this problem: it went fullscreen 10 times out of 10.

### Problem 2: macOS native fullscreen breaks mouse actions

With `fullscreen_window()` working, headed runs failed 4 tests every time, in 3 of 3 full runs. They're exactly the tests that use `ActionChains`:

| Test | Fullscreen | Fullscreen + 1s wait | Fullscreen + 2s wait | Maximized |
|---|---|---|---|---|
| `test_context_menu` | 0/3 | 3/3 | 3/3 | 3/3 |
| `test_slider` | 0/3 | 3/3 | 3/3 | 3/3 |
| `test_drag_and_drop` | 0/3 | 2/3 | 3/3 | 3/3 |
| `test_hovers` | 0/3 | 0/3 | 0/3 | 3/3 |
| Time per run (these 4 tests) | ~11s | ~12s | ~15.5s | ~9.4s |

- **Most failures come from the fullscreen animation.** macOS moves a fullscreen window into its own desktop space with an animation that keeps running after `fullscreen_window()` returns. Mouse actions performed during it miss. A fixed pause fixes three of the four tests.
- **Hovers fails in fullscreen no matter how long you wait.** Why is unknown. It isn't the window's size, because a maximized window, which is nearly as large, passes. Something about macOS's separate fullscreen space seems to be the cause.
- **A maximized window stays in the normal desktop space**, with no animation that affects tests. All four passed with no wait.

### Headless has no real screen

Headless Chrome pretends the screen is 800×600, so maximizing (or fullscreen) alone gives an 800×600 window. `--screen-info={1920x1080}` gives headless Chrome a 1920×1080 virtual screen to fill. `--window-size=1920,1080` doesn't work: resizing to the screen shrinks it back to 800×600.

## Options considered

| Option | Headed result | Headed window | Headless viewport |
|---|---|---|---|
| `--start-fullscreen` flag | fullscreen only 1 of 5 times with Terminal focused | 1200×950 when it fails | 1920×1024 |
| `fullscreen_window()` | always fullscreen, but 4 `ActionChains` tests fail | 1728×1084 | 1920×1024 |
| `fullscreen_window()` + fixed pause | 2s fixes 3 of the 4, `test_hovers` still fails, adds ~2s per test | 1728×1084 | 1920×1024 |
| **`maximize_window()`** | **always maximized, all tests pass, no pause** | **1728×994** | **1920×937** |
| `--start-maximized` flag | always maximized (3 of 3), not tried with the `ActionChains` tests | 1728×994 | 1920×937 |

A general "wait until the page has settled" check (network, DOM, and layout quiet for a moment) was also discussed as a way to guard against any not-ready state, not just this animation. It was set aside. Maximize removes the problem that prompted it, and whether it would catch this animation was never tested.

## Decision

- **Keep `--screen-info={1920x1080}` for headless**, because headless Chrome's default virtual screen is only 800×600, so maximizing without it gives an 800×600 window.
- **Drop `--start-fullscreen`**, because macOS ignores Chrome's startup fullscreen request when another app, like the terminal running pytest, has focus at launch.
- **Call `driver.maximize_window()` instead of going fullscreen**, because macOS's fullscreen animation and separate desktop space made mouse actions (right-click, click at an offset, drag, hover) miss or fail, while a maximized window passed every test with no wait.
- **Use the `maximize_window()` method rather than the `--start-maximized` flag**, because the method is what was tested with the `ActionChains` tests.
- **Call it inside `get_driver()`**, so every driver gets it, whether it comes from the `driver` fixture or a direct call.
- **Call it right after the driver is created, before the first navigation**, so pages load at full size from the start.

## Consequences

- Headed runs on macOS are reliably maximized, whichever app has focus, and tests don't have to wait for an animation.
- Pages get slightly less room than fullscreen: the macOS menu bar and Dock stay visible headed (994 vs. 1084 tall), and Chrome's toolbar stays visible headless (a 937 vs. 1024 tall viewport).
- Why `test_hovers` fails in native fullscreen is still unknown. If fullscreen is ever reconsidered, retest headed runs with a terminal focused, and include the `ActionChains` tests.
