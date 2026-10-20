from adapters.base import ScreenplayAdapter
from adapters.generic_screenplay import GenericScreenplayAdapter
from adapters.playwright_screenplay import PlaywrightScreenplayAdapter
from adapters.selenium_screenplay import SeleniumScreenplayAdapter
from adapters.serenity_screenplay import SerenityScreenplayAdapter
from core.project_config import ProjectConfig

_ADAPTERS: dict[str, type[ScreenplayAdapter]] = {
    "serenity": SerenityScreenplayAdapter,
    "serenity_bdd": SerenityScreenplayAdapter,
    "playwright": PlaywrightScreenplayAdapter,
    "selenium": SeleniumScreenplayAdapter,
    "generic": GenericScreenplayAdapter,
    "generic_screenplay": GenericScreenplayAdapter,
}


def create_adapter(config: ProjectConfig) -> ScreenplayAdapter:
    adapter_type = _ADAPTERS.get(
        config.framework.casefold(),
        GenericScreenplayAdapter,
    )
    return adapter_type(config)
