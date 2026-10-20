import re

from adapters.generic_screenplay.adapter import GenericScreenplayAdapter


class SeleniumScreenplayAdapter(GenericScreenplayAdapter):
    """Adapter for Selenium-based Screenplay projects."""

    target_patterns = (
        *GenericScreenplayAdapter.target_patterns,
        re.compile(
            r"""(?:By\.)?(?:cssSelector|xpath|id|name)\s*\(\s*["']([^"']+)["']"""
        ),
    )
