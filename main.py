import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from config import BOT_TOKEN, ADMIN_ID, CARD_NUMBER, CARD_NAME, PHONE_NUMBER, PRICE
from database import init_db, add_user, set_paid, is_paid, get_all_users
from buttons import main_menu, admin_confirm, admin_panel

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

VIDEO_ID = "BAACAgIAAxkBAAOpaaQFhkFgHIeufb-h-jUvMm_7lWkAAsuRAAI67CBJYzW3fd1VkGo6BA"

# ===== STATE =====
class PayState(StatesGroup):
    waiting_screenshot = State()
    broadcast = State()

# ===== START =====
@dp.message(Command("start"))
async def start_handler(message: types.Message):
    add_user(message.from_user.id, message.from_user.username)
    await message.answer(
        f"Assalomu alaykum {message.from_user.full_name} 👋\n"
        "Kurs botiga xush kelibsiz.",
        reply_markup=main_menu()
    )

# ===== OPTIMIZE =====
@dp.callback_query(F.data == "optimize")
async def optimize_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    if is_paid(callback.from_user.id):
        await callback.message.answer_video(
            video=VIDEO_ID,
            protect_content=True
        )
    else:
        await callback.message.answer(
            f"❌ Darslikni olish uchun avval to'lov qilishingiz kerak!\n\n"
            f"💰 Narx: {PRICE}\n\n"
            f"💳 To'lov uchun ma'lumotlar:\n\n"
            f"Karta: {CARD_NUMBER}\n"
            f"Ism: {CARD_NAME}\n"
            f"Telefon: {PHONE_NUMBER}\n\n"
            "To'lov qilgach screenshot yuboring."
        )
        await state.set_state(PayState.waiting_screenshot)

# ===== TO'LOV TUGMASI =====
@dp.callback_query(F.data == "pay")
async def pay_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(
        f"💰 Narx: {PRICE}\n\n"
        f"💳 To'lov uchun ma'lumotlar:\n\n"
        f"Karta: {CARD_NUMBER}\n"
        f"Ism: {CARD_NAME}\n"
        f"Telefon: {PHONE_NUMBER}\n\n"
        "To'lov qilgach screenshot yuboring."
    )
    await state.set_state(PayState.waiting_screenshot)

# ===== SCREENSHOT QABUL =====
@dp.message(PayState.waiting_screenshot, F.photo)
async def get_screenshot(message: types.Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await bot.send_photo(
        ADMIN_ID,
        photo,
        caption=f"💳 To'lov screenshot\nUser: {message.from_user.id} (@{message.from_user.username})",
        reply_markup=admin_confirm(message.from_user.id)
    )
    await message.answer("✅ Screenshot adminga yuborildi. Tasdiqlanishini kuting.")
    await state.clear()

# ===== ADMIN TASDIQLASH =====
@dp.callback_query(F.data.startswith("confirm_"))
async def confirm_payment(callback: types.CallbackQuery):
    await callback.answer()
    user_id = int(callback.data.split("_")[1])
    set_paid(user_id)
    await bot.send_message(user_id, "✅ To'lov tasdiqlandi! Endi darslikni olishingiz mumkin.")
    await callback.message.edit_text("To'lov tasdiqlandi ✅")

@dp.callback_query(F.data.startswith("reject_"))
async def reject_payment(callback: types.CallbackQuery):
    await callback.answer()
    user_id = int(callback.data.split("_")[1])
    await bot.send_message(user_id, "❌ To'lov xato! Iltimos qayta urinib ko'ring.")
    await callback.message.edit_text("To'lov rad etildi ❌")

# ===== ADMIN PANEL =====
@dp.message(Command("admin"))
async def admin_panel_handler(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("🛠 Admin Panel", reply_markup=admin_panel())

@dp.callback_query(F.data == "show_users")
async def show_users(callback: types.CallbackQuery):
    await callback.answer()
    users = get_all_users()
    text = "👥 Start bosgan foydalanuvchilar:\n\n"
    for uid, uname, paid in users:
        status = "To'lov qildi ✅" if paid else "To'lov qilmagan ❌"
        text += f"{uname} ({uid}) - {status}\n"
    await callback.message.answer(text)

@dp.callback_query(F.data == "send_message")
async def send_message_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Xabar matnini yozing:")
    await state.set_state(PayState.broadcast)

@dp.message(PayState.broadcast)
async def broadcast_message(message: types.Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await state.clear()
        return
    users = get_all_users()
    for uid, _, _ in users:
        try:
            await bot.send_message(uid, message.text)
        except:
            pass
    await message.answer("✅ Xabar barcha foydalanuvchilarga yuborildi.")
    await state.clear()

# ===== RUN =====
async def main():
    init_db()
    print("Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())