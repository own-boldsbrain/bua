from bua.computers.default.local_playwright import LocalPlaywrightBrowser
from bua.computers.default.browserbase import BrowserbaseBrowser
from bua.computers.default.notte import NotteBrowser

computers_config = {
    "local-playwright": LocalPlaywrightBrowser,
    "notte": NotteBrowser,
    "browserbase": BrowserbaseBrowser,
}

