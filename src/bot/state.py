from aiogram.fsm.state import State, StatesGroup


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


class BotPaymentsSorting(StatesGroup):
    sorting = State()
    category_suggestion = State()
