import re

from adapters.generic_screenplay.adapter import GenericScreenplayAdapter


class PlaywrightScreenplayAdapter(GenericScreenplayAdapter):
    """Adapter for Playwright-based Screenplay projects."""

    target_patterns = (
        *GenericScreenplayAdapter.target_patterns,
        re.compile(
            r"""page\.(?:get_by_label|getByLabel)\s*\(\s*["']([^"']+)["']"""
        ),
    )
