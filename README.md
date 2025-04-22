# Browser Using Agent

Get started building a Browser Using Agent (BUA) with the Notte API.

## Set Up & Run

Set up python env and install dependencies.

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run CLI to let BUA use a local browser window, using [playwright](https://playwright.dev/). (Stop with CTRL+C)

```shell
python -m bua
```

> [!NOTE]  
> The first time you run this, if you haven't used Playwright before, you will be prompted to install dependencies. Execute the command suggested, which will depend on your OS.

Other included sample [browser environments](#browser-environments):

- [Notte](https://www.notte.cc) (remote browser, requires account)
- [Browserbase](https://www.browserbase.com/) (remote browser, requires account)
- ...or implement your own `Browser`!

## Overview

The browser use tool and model are available via the Responses API. At a high level, BUA will look at a screenshot and the DOM elements of the browser interface and recommend actions. You can learn more about this tool in the Browser Using Agent guide.

## Abstractions

This repository defines two lightweight abstractions to make interacting with BUA agents more ergonomic. Everything works without them, but they provide a convenient separation of concerns.

| Abstraction | File                   | Description                                                                                                                                                                                               |
| ----------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Browser`   | `browsers/browsers.py` | Defines a `Browser` interface for various environments (local desktop, remote browser, etc.). An implementation of `Browser` is responsible for executing any `browser_action` sent by BUA (clicks, etc). |
| `Agent`     | `agent/agent.py`       | Simple, familiar agent loop – implements `run_full_turn()`, which just keeps calling the model until all browser actions and function calls are handled.                                                  |

## CLI Usage

The CLI (`cli.py`) is the easiest way to get started with BUA. It accepts the following arguments:

- `--browser`: The browser environment to use. See the [Browser Environments](#browser-environments) section below for options. By default, the CLI will use the `local-playwright` environment.
- `--input`: The initial input to the agent (optional: the CLI will prompt you for input if not provided)
- `--debug`: Enable debug mode.
- `--show`: Show images (screenshots) during the execution.
- `--start-url`: Start the browsing session with a specific URL (only for browser environments)

## Drop in replacement for computer-use

BUA can work with any `Browser` environment that can handle BUA actions.
If your `Browser` relied on playwright, they are even already implemented!

Not convinced? You can run a task using computer-use-preview instead, and compare with bua:

```
python -m bua --model cua
```

## Browser Environments

This sample app provides a set of implemented `Browser` examples, but feel free to add your own!

| Browser           | Option           | Type      | Description                | Requirements                                                  |
| ----------------- | ---------------- | --------- | -------------------------- | ------------------------------------------------------------- |
| `LocalPlaywright` | local-playwright | `browser` | Local browser window       | [Playwright SDK](https://playwright.dev/)                     |
| `Notte`           | notte            | `browser` | Remote browser environment | [Notte](https://www.notte.cc/) API key in `.env`              |
| `Browserbase`     | browserbase      | `browser` | Remote browser environment | [Browserbase](https://www.browserbase.com/) API key in `.env` |

Using the CLI, you can run the sample app with different browser environments using the options listed above:

```shell
python -m bua --show --browser <browser-option>
```

For example, to run the sample app with the `Notte` browser environment, you can run:

```shell
python -m bua --show --browser notte
```

## Function Calling

We don't currently support function calling, but if it's something that you are looking forward to, feel free to let us know!

