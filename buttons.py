from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="😎 Optimize", callback_data="optimize")],
        [InlineKeyboardButton(text="💳 To'lov qilish", callback_data="pay")]
    ])
    return kb

def admin_confirm(user_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Tasdiqlash", callback_data=f"confirm_{user_id}")],
        [InlineKeyboardButton(text="❌ Rad etish", callback_data=f"reject_{user_id}")]
    ])
    return kb

def admin_panel():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👥 Foydalanuvchilarni ko'rish", callback_data="show_users")],
        [InlineKeyboardButton(text="📢 Xabar yuborish", callback_data="send_message")]
    ])
    return kb