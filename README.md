![bua-banner (1)](https://github.com/user-attachments/assets/8c21e357-742b-4693-950d-04ac73d8d72d)

## Your fast track to a browser using agent

![2025-04-23 11-46-22](https://github.com/user-attachments/assets/9774aa35-c7b3-45a2-949e-e7a7552cda83)

Create an account over on [console.notte.cc](https://console.notte.cc/start), and create an api key.

Load your api key as an environment variable (or create a .env file, following the example in .env.example). 
```
export NOTTE_API_KEY=<YOUR_API_KEY>
```

Set up a python virtual environment and install dependencies (pypi package coming soon).

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run the CLI to let BUA start a local browser window, using [playwright](https://playwright.dev/). (Stop with CTRL+C)

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

BUA acts similarly to tha typical [computer-use](https://platform.openai.com/docs/models/computer-use-preview) completion model. At a high level, BUA will look at a screenshot and the DOM elements of the browser interface and output an action, than can easily be executed from any browser driver.

## Abstractions

This repository defines two lightweight abstractions to make interacting with BUA agents more ergonomic. Everything works without them, but they provide a convenient separation of concerns.

| Abstraction | File                   | Description                                                                                                                                                                                               |
| ----------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Browser`   | `computers/computer.py` | Defines a `Browser` interface for various environments (local desktop, remote browser, etc.). An implementation of `Browser` is responsible for executing any `browser_action` sent by BUA (clicks, etc). Any CUA computer can also implement the browser interface if they which to be compatible.|
| `Agent`     | `agent/agent.py`       | Simple, familiar agent loop – implements `run_full_turn()`, which just keeps calling the model until all browser actions and function calls are handled.                                                  |

## CLI Usage

The CLI (`cli.py`) is the easiest way to get started with BUA. It accepts the following arguments:

- `--computer`: The browser environment to use. See the [Browser Environments](#browser-environments) section below for options. By default, the CLI will use the `local-playwright` environment.
- `--model`: The computer using model to use. Currently compatible with `bua` and `cua`.

## Drop in replacement for computer-use

BUA can work with any `Browser` environment that can handle BUA actions.
If your `Browser` relied on playwright, they are even already implemented!

Not convinced? You can run a task using [computer-use-preview](https://platform.openai.com/docs/models/computer-use-preview) instead, and compare with bua:

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
python -m bua --computer <browser-option>
```

For example, to run the sample app, and have your browser hosted by `Notte`, you can run:

```shell
python -m bua --browser notte
```

## Function Calling

We don't currently support function calling, but if it's something that you are looking forward to, feel free to let us know!

