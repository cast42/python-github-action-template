"""Load page of URL, accept all cookies and take a screenshot"""

import logging
import logging.handlers
from datetime import datetime, timezone

# import pytz
from zoneinfo import ZoneInfo
from pathlib import Path
from playwright.sync_api import sync_playwright

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger_file_handler = logging.handlers.RotatingFileHandler(
        "status.log",
        maxBytes=1024 * 1024,
        backupCount=1,
        encoding="utf8",
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    logger_file_handler.setFormatter(formatter)
    logger.addHandler(logger_file_handler)

    dst = Path("./shots")  # Directory to store resulting png images in.
    dst.mkdir(exist_ok=True)
    # url = "https://www.google.com/maps/@50.9503538,4.7123571,734m/data=!5m1!1e1"
    URL_RODENBACHLAAN = (
        "https://www.google.com/maps/@50.9492399,4.7079242,18z/data=!5m1!1e1"
    )
    URL_STATIONSTRAAT = (
        "https://www.google.com/maps/@50.9495439,4.714087,18.79z/data=!5m1!1e1"
    )
    URL_TORENSTRAAT = (
        "https://www.google.com/maps/@50.9509771,4.7137899,18.79z/data=!5m1!1e1"
    )
    URL_PROVINCIEBAAN = (
        "https://www.google.com/maps/@50.9509773,4.7104413,18.81z/data=!5m1!1e1"
    )

    URLS = [URL_RODENBACHLAAN, URL_STATIONSTRAAT, URL_TORENSTRAAT, URL_PROVINCIEBAAN]
    STREETNAMES = ["rodenbachlaan", "stationstraat", "torenstraat", "provinciebaan"]

    with sync_playwright() as p:
        browser_type = p.chromium
        browser = browser_type.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(URLS[0])
        for i, el in enumerate(page.get_by_label("Accept all").all()):
            try:
                el.click()
            except Exception as e:
                logging.debug(f"Clicked {i}th element: {str(e)}")
        page.wait_for_load_state("networkidle")
        for url, streetname in zip(URLS, STREETNAMES):
            page.goto(url)
            page.wait_for_load_state("networkidle")
            page.screenshot(path=shot_file.as_posix())
            now_utc = datetime.now(timezone.utc)
            now_local = now_utc.astimezone(ZoneInfo("Europe/Brussels"))
            timestr = now_local.strftime("%Y%m%d-%H%M%S")
            shot_file = dst / f"rotselaar_{streetname}_{timestr}.png"
            logger.info(f"Took shot {shot_file.as_posix()} on {timestr}.")
        context.close()
        browser.close()
