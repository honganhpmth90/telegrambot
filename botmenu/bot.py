# -*- coding: utf-8 -*-
from collections import OrderedDict
import inspect

from telegram import ReplyKeyboardMarkup
from botmenu.menu import MagicMenu


class MagicFunction:
    menu_storage = dict()
    custom_menu = OrderedDict([])

    def set_custom_menu(self, menu):
        self.custom_menu = menu

    def gen_keyboard(self, update):
        return ReplyKeyboardMarkup(
            self.get_markup(update),
            resize_keyboard=True
        )

    def get_markup(self, update):
        self.__create_storage(update)
        chat_id = update.effective_chat.id
        menu = self.menu_storage[chat_id]
        keyboard = menu.get_keyboard()
        return keyboard

    async def text_menu(self, bot, update):
        """Gọi action tương ứng trong menu.

        Action có thể là sync hoặc async.
        """
        self.__create_storage(update)
        chat_id = update.effective_chat.id
        menu = self.menu_storage[chat_id]

        menu.set_state(update.message.text)
        action = menu.get_action(self)   # ví dụ self.inventory, self.magic, ...

        result = action(bot, update)
        # nếu action là coroutine -> await
        if inspect.isawaitable(result):
            return await result
        return result

    def __create_storage(self, update):
        chat_id = update.effective_chat.id
        if chat_id not in self.menu_storage:
            self.menu_storage[chat_id] = MagicMenu(
                self.custom_menu,
                chat_id
            )
