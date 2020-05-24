from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


# Main_keyboard---------------------------------------------------------------------------------------------------------
# Commands
MAIN_COMMAND_INFO = 'информация'
MAIN_COMMAND_PDT = 'pdt response'
MAIN_COMMAND_PROMOTION = 'заработок и продвижение'
# Init_keyboard
MAIN_MARKUP = ReplyKeyboardMarkup(resize_keyboard=True)
# Init_buttons
MAIN_BUTTON_INFO = KeyboardButton(MAIN_COMMAND_INFO)
MAIN_BUTTON_PDT_RESPONSE = KeyboardButton(MAIN_COMMAND_PDT)
MAIN_BUTTON_PROMOTION = KeyboardButton(MAIN_COMMAND_PROMOTION)
# Add_buttons
MAIN_MARKUP.add(MAIN_BUTTON_INFO, MAIN_BUTTON_PDT_RESPONSE)
MAIN_MARKUP.add(MAIN_BUTTON_PROMOTION)
# ----------------------------------------------------------------------------------------------------------------------


# Inline_keyboards------------------------------------------------------------------------------------------------------
# Inline_main_keyboard--------------------------------------------------------------------------------------------------
# Commands
INLINE_COMMAND_MANAGE_EVENTS = 'Manage Events'
INLINE_COMMAND_MANAGE_USERS = 'Manage Users'
# Init_keyboard
INLINE_MAIN_MARKUP = InlineKeyboardMarkup(row_width=1)
# Init_buttons
INLINE_BUTTON_MANAGE_EVENTS = InlineKeyboardButton(INLINE_COMMAND_MANAGE_EVENTS,
                                                   callback_data=INLINE_COMMAND_MANAGE_EVENTS)
INLINE_BUTTON_MANAGE_USERS = InlineKeyboardButton(INLINE_COMMAND_MANAGE_USERS,
                                                  callback_data=INLINE_COMMAND_MANAGE_USERS)
# Add_buttons
INLINE_MAIN_MARKUP.add(INLINE_BUTTON_MANAGE_EVENTS, INLINE_BUTTON_MANAGE_USERS)
# ----------------------------------------------------------------------------------------------------------------------

# Inline_manage_events_keyboard-----------------------------------------------------------------------------------------
# Commands
INLINE_COMMAND_UPDATE_EVENT = 'Update Event'
INLINE_COMMAND_DEL_ONE_EVENT = 'Clean one Event'
INLINE_COMMAND_DEL_DAY = 'Clean all events in day'
INLINE_COMMAND_DEL_ALL_EVENTS = 'Clean ALL Events'
# Init_keyboard
INLINE_MANAGE_EVENTS_MARKUP = InlineKeyboardMarkup(row_width=2)
# Init_buttons
INLINE_BUTTON_UPDATE_EVENT = InlineKeyboardButton(INLINE_COMMAND_UPDATE_EVENT,
                                                  callback_data=INLINE_COMMAND_UPDATE_EVENT)
INLINE_BUTTON_DEL_ONE_EVENT = InlineKeyboardButton(INLINE_COMMAND_DEL_ONE_EVENT,
                                                   callback_data=INLINE_COMMAND_DEL_ONE_EVENT)
INLINE_BUTTON_DEL_DAY = InlineKeyboardButton(INLINE_COMMAND_DEL_DAY, callback_data=INLINE_COMMAND_DEL_DAY)
INLINE_BUTTON_DEL_ALL_EVENTS = InlineKeyboardButton(INLINE_COMMAND_DEL_ALL_EVENTS,
                                                    callback_data=INLINE_COMMAND_DEL_ALL_EVENTS)
# Add_buttons
INLINE_MANAGE_EVENTS_MARKUP.add(INLINE_BUTTON_UPDATE_EVENT, INLINE_BUTTON_DEL_ONE_EVENT, INLINE_BUTTON_DEL_DAY,
                                INLINE_BUTTON_DEL_ALL_EVENTS)
# ----------------------------------------------------------------------------------------------------------------------

# Inline_manage_users_keyboard------------------------------------------------------------------------------------------
# Commands
INLINE_COMMAND_UPDATE_USER = 'Update user'
INLINE_COMMAND_GET_ADMINS = 'Show admins'
INLINE_COMMAND_GET_PDTS = 'Show PDTs'
INLINE_COMMAND_GET_PROMOTIONS = 'Show promos'
INLINE_COMMAND_GET_ALL = 'Show ALL users'
# Init_keyboard
INLINE_MANAGE_USERS_MARKUP = InlineKeyboardMarkup(row_width=3)
# Init_buttons
INLINE_BUTTON_UPDATE_USER = InlineKeyboardButton(INLINE_COMMAND_UPDATE_USER, callback_data=INLINE_COMMAND_UPDATE_USER)
INLINE_BUTTON_GET_ADMINS = InlineKeyboardButton(INLINE_COMMAND_GET_ADMINS, callback_data=INLINE_COMMAND_GET_ADMINS)
INLINE_BUTTON_GET_PDTS = InlineKeyboardButton(INLINE_COMMAND_GET_PDTS, callback_data=INLINE_COMMAND_GET_PDTS)
INLINE_BUTTON_GET_PROMOTIONS = InlineKeyboardButton(INLINE_COMMAND_GET_PROMOTIONS,
                                                    callback_data=INLINE_COMMAND_GET_PROMOTIONS)
INLINE_BUTTON_GET_ALL = InlineKeyboardButton(INLINE_COMMAND_GET_ALL, callback_data=INLINE_COMMAND_GET_ALL)
# Add_buttons
INLINE_MANAGE_USERS_MARKUP.add(INLINE_BUTTON_UPDATE_USER)
INLINE_MANAGE_USERS_MARKUP.add(INLINE_BUTTON_GET_ADMINS, INLINE_BUTTON_GET_PDTS, INLINE_BUTTON_GET_PROMOTIONS)
INLINE_MANAGE_USERS_MARKUP.add(INLINE_BUTTON_GET_ALL)
# ----------------------------------------------------------------------------------------------------------------------

# Inline_update_users_keyboard------------------------------------------------------------------------------------------
# Commands
INLINE_COMMAND_CHANGE_ADD_USER = 'Change or add user'
INLINE_COMMAND_DEL_USER = 'Delete user'
# Init_keyboard
INLINE_UPDATE_USER_MARKUP = InlineKeyboardMarkup(row_width=1)
# Init_buttons
INLINE_BUTTON_CHANGE_ADD_USER = InlineKeyboardButton(INLINE_COMMAND_CHANGE_ADD_USER,
                                                     callback_data=INLINE_COMMAND_CHANGE_ADD_USER)
INLINE_BUTTON_DEL_USER = InlineKeyboardButton(INLINE_COMMAND_DEL_USER, callback_data=INLINE_COMMAND_DEL_USER)
# Add_buttons
INLINE_UPDATE_USER_MARKUP.add(INLINE_BUTTON_CHANGE_ADD_USER, INLINE_BUTTON_DEL_USER)
# ----------------------------------------------------------------------------------------------------------------------

# Inline_permissions_keyboard-------------------------------------------------------------------------------------------
# Commands
INLINE_COMMAND_IS_ADMIN = 'Switch: admin'
INLINE_COMMAND_IS_PDT = 'Switch: pdt'
INLINE_COMMAND_IS_PROMOTION = 'Switch: subscription'
INLINE_COMMAND_END_EDIT = 'End edit user permissions'
# Init_keyboards
INLINE_SUPERUSER_MARKUP = InlineKeyboardMarkup(row_width=1)
INLINE_ADMIN_MARKUP = InlineKeyboardMarkup(row_width=1)
# Init_buttons
INLINE_BUTTON_IS_ADMIN = InlineKeyboardButton(INLINE_COMMAND_IS_ADMIN, callback_data=INLINE_COMMAND_IS_ADMIN)
INLINE_BUTTON_IS_PDT = InlineKeyboardButton(INLINE_COMMAND_IS_PDT, callback_data=INLINE_COMMAND_IS_PDT)
INLINE_BUTTON_IS_PROMOTION = InlineKeyboardButton(INLINE_COMMAND_IS_PROMOTION,
                                                  callback_data=INLINE_COMMAND_IS_PROMOTION)
INLINE_BUTTON_END_EDIT = InlineKeyboardButton(INLINE_COMMAND_END_EDIT, callback_data=INLINE_COMMAND_END_EDIT)
# Add_buttons
INLINE_SUPERUSER_MARKUP.add(INLINE_BUTTON_IS_ADMIN, INLINE_BUTTON_IS_PDT, INLINE_BUTTON_IS_PROMOTION,
                            INLINE_BUTTON_END_EDIT)
INLINE_ADMIN_MARKUP.add(INLINE_BUTTON_IS_PDT, INLINE_BUTTON_IS_PROMOTION, INLINE_BUTTON_END_EDIT)
# ----------------------------------------------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------------------------------------------
