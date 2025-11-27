# -*- coding: utf-8 -*-
import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from botmenu.buttons import PrevButton
from botmenu.bot import MagicFunction

my_custom_menu = {
    'menu': {
        'magic': '🔮Hướng dẫn sử dụng',
        'magic_nested': {
            'fire': '🔥 Hướng dẫn chơi game 1',
            'cold': '❄️ Hướng dẫn chơi game 2',
            'prev': PrevButton('◀️ Quay lại')
        },
        'inventory': '⛏ Cài đặt',
        'inventory_nested': {
            'potion': '⚗ Cài đặt game',
            'armor': '🛡 Cài đặt tài khoản',
            'weapon': '⚔ Cài đặt khác',
            'prev': PrevButton('◀️Quay lại'),
            'weapon_nested': {
                'sword': '🗡 Cài đặt khác 1',
                'knife': '🔪 Cài đặt khác 2',
                'prev': PrevButton('◀️ Quay lại')
            }
        },
    }
}


class TestBot(MagicFunction):

    # /start
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            text='Chào mừng bạn đến với game !',
            reply_markup=self.gen_keyboard(update),
        )

    async def inventory(self, bot, update: Update):
        await update.message.reply_text(
            text='Lập trình viên với hơn 5 năm kinh nghiệm chuyên sâu ',
            reply_markup=self.gen_keyboard(update),
        )

    async def potion(self, bot, update: Update):
        text = 'Lập trình viên với hơn 5 năm kinh nghiệm chuyên sâu :(' + os.linesep
        text += 'Lập trình viên với hơn 5 năm kinh nghiệm chuyên sâu ' + os.linesep
        await update.message.reply_text(
            text=text,
            reply_markup=self.gen_keyboard(update),
        )

    async def armor(self, bot, update: Update):
        text = 'Lập trình viên với hơn 5 năm kinh nghiệm chuyên sâu:(' + os.linesep
        text += 'Lập trình viên với hơn 5 năm kinh nghiệm chuyên sâu ?' + os.linesep
        await update.message.reply_text(
            text=text,
            reply_markup=self.gen_keyboard(update),
        )

    async def weapon(self, bot, update: Update):
        await update.message.reply_text(
            text='Lập trình viên với hơn 5 năm kinh nghiệm chuyên sâu ?',
            reply_markup=self.gen_keyboard(update),
        )

    async def magic(self, bot, update: Update):
        await update.message.reply_text(
            text='Lập trình viên với hơn 5 năm kinh nghiệm chuyên sâu ?',
            reply_markup=self.gen_keyboard(update),
        )

    async def sword(self, bot, update: Update):
        await update.message.reply_text(
            text='Cài đặt khác 1 🗡',
            reply_markup=self.gen_keyboard(update),
        )

    async def knife(self, bot, update: Update):
        await update.message.reply_text(
            text='🔪Caài đặt 2',
            reply_markup=self.gen_keyboard(update),
        )

    async def fire(self, bot, update: Update):
        await update.message.reply_text(
            text='Huong dan choi 1',
            reply_markup=self.gen_keyboard(update),
        )

    async def cold(self, bot, update: Update):
        await update.message.reply_text(
            text='Huong dan choi 2',
            reply_markup=self.gen_keyboard(update),
        )

    async def prev(self, bot, update: Update):
        await update.message.reply_text(
            text='Quay lại...',
            reply_markup=self.gen_keyboard(update),
        )

    # Handler text chính: gửi mọi message text vào hệ thống menu
    async def text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.text_menu(context.bot, update)

    async def error_handler(self, update: object, context: ContextTypes.DEFAULT_TYPE):
        # log đơn giản
        print(f"Bạn chọn : {context.error}")

    def run(self, token: str):
        self.set_custom_menu(my_custom_menu)

        app = (
            ApplicationBuilder()
            .token(token)
            .build()
        )

        # /start
        app.add_handler(CommandHandler('start', self.start))
        # tất cả TEXT không phải lệnh → menu
        app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.text)
        )

        app.add_error_handler(self.error_handler)

        app.run_polling()


if __name__ == '__main__':
    TOKEN = "toke"
    TestBot().run(TOKEN)
