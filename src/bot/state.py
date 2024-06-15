from aiogram.fsm.state import StatesGroup, State


class BotStates(StatesGroup):
    main_menu = State()
    statistics = State()
    settings = State()
    view_statistics = State()
    period_statistics = State()


class BotCategorySettingsStates(StatesGroup):
    settings_category = State()
    add_category = State()
    edit_category = State()
    new_name_for_category = State()
    delete_category = State()
    deletion_confirm = State()
