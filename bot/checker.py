import re
import xml.etree.ElementTree as ET
import logging

import aiohttp

logger = logging.getLogger(__name__)

# API expects full language names
LANG_MAP = {
    "ru": "russian",
    "en": "english",
    "it": "italian",
}

SUBMIT_LABELS = {
    "ru": "Ввод",
    "en": "Send",
    "it": "Invia",
}

# Each language has its own prefix before the actual status
STATUS_PREFIXES = [
    "На каком этапе работы вид на жительство:",    # ru
    "Residence permit position:",                   # en
    "Stato del suo permesso di soggiorno:",         # it
]

RSS_URL = "https://questure.poliziadistato.it/servizio/stranieri"


def build_check_url(case_number: str, lang: str) -> str:
    api_lang = LANG_MAP.get(lang, "english")
    return f"{RSS_URL}?lang={api_lang}&pratica={case_number}"


async def check_status(case_number: str, lang: str) -> str | None:
    """Query the police RSS feed and return the status text, or None on error."""
    submit = SUBMIT_LABELS.get(lang, SUBMIT_LABELS["en"])
    api_lang = LANG_MAP.get(lang, "english")
    params = {
        "lang": api_lang,
        "pratica": case_number,
        "invia": submit,
        "mime": "4",
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(RSS_URL, params=params, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    logger.warning("HTTP %s for case %s", resp.status, case_number)
                    return None
                text = await resp.text()
    except Exception:
        logger.exception("Network error checking case %s", case_number)
        return None

    try:
        # Fix bare '&' not followed by amp;/lt;/gt;/quot;/apos;/#
        text = re.sub(r"&(?!amp;|lt;|gt;|quot;|apos;|#)", "&amp;", text)
        root = ET.fromstring(text)
        item = root.find(".//channel/item/description")
        if item is not None and item.text:
            status = item.text.strip()
            # Strip the language-specific prefix
            for prefix in STATUS_PREFIXES:
                if status.lower().startswith(prefix.lower()):
                    status = status[len(prefix):].strip()
                    break
            # Clean HTML: <br /> → newline, strip remaining tags
            status = re.sub(r"<br\s*/?>", "\n", status)
            status = re.sub(r"<[^>]+>", "", status)
            # Collapse multiple whitespace/newlines
            status = re.sub(r"\n\s*\n", "\n", status).strip()
            return status
        return None
    except ET.ParseError:
        logger.exception("XML parse error for case %s", case_number)
        return None
