import pytest
from app.app import TypingApp
from app.screens.command_palette import CommandPalette
from app.screens.result import ResultScreen
from app.widgets.typing_area import TypingArea


@pytest.mark.asyncio
async def test_app_starts_and_types():
    app = TypingApp()
    async with app.run_test() as pilot:
        await pilot.pause()
        typing_area = app.screen.query_one(TypingArea)
        assert typing_area is not None
        assert typing_area.session.lifecycle.value == "idle"

        # Type first character of target
        target_char = typing_area.state.target[0]
        await pilot.press(target_char)
        await pilot.pause()

        assert typing_area.session.lifecycle.value == "running"
        assert typing_area.state.typed == target_char


@pytest.mark.asyncio
async def test_app_restart_shortcut():
    app = TypingApp()
    async with app.run_test() as pilot:
        await pilot.pause()
        typing_area = app.screen.query_one(TypingArea)

        # Type something
        await pilot.press("h")
        await pilot.pause()
        assert typing_area.state.typed != ""

        # Press ctrl+r to restart
        await pilot.press("ctrl+r")
        await pilot.pause()

        new_typing_area = app.screen.query_one(TypingArea)
        assert new_typing_area.session.lifecycle.value == "idle"
        assert new_typing_area.state.typed == ""


@pytest.mark.asyncio
async def test_app_test_completion_flow():
    app = TypingApp()
    async with app.run_test() as pilot:
        await pilot.pause()
        typing_area = app.screen.query_one(TypingArea)

        # Use a short custom target by resetting with 1 word
        typing_area.reset_test(new_words=["hi"])
        await pilot.pause()

        # Type "hi"
        await pilot.press("h")
        await pilot.press("i")
        await pilot.pause()

        # Should have pushed ResultScreen
        assert isinstance(app.screen, ResultScreen)

        # Press Enter to start next test
        await pilot.press("enter")
        await pilot.pause()

        # Should be back on TypingScreen
        new_area = app.screen.query_one(TypingArea)
        assert new_area.session.lifecycle.value == "idle"


@pytest.mark.asyncio
async def test_app_abort_on_escape():
    app = TypingApp()
    async with app.run_test() as pilot:
        await pilot.pause()
        typing_area = app.screen.query_one(TypingArea)

        # Start typing
        await pilot.press(typing_area.state.target[0])
        await pilot.pause()
        assert typing_area.session.lifecycle.value == "running"

        # Press Escape
        await pilot.press("escape")
        await pilot.pause()
        assert typing_area.session.lifecycle.value == "aborted"


@pytest.mark.asyncio
async def test_app_command_palette_toggle():
    app = TypingApp()
    async with app.run_test() as pilot:
        await pilot.pause()

        # Press Ctrl+K
        await pilot.press("ctrl+k")
        await pilot.pause()

        assert isinstance(app.screen, CommandPalette)

        # Cancel with Escape
        await pilot.press("escape")
        await pilot.pause()

        assert not isinstance(app.screen, CommandPalette)
