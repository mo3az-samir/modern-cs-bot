import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())



from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ✨ حط التوكن بتاعك هنا
TOKEN = "8587194106:AAHXquYldB0-oRc_nqsqDy0CuocrHSAeQqQ"

# 🎓 رسالة البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name  # جلب اسم المستخدم
    keyboard = [[InlineKeyboardButton("🧑‍💻 سنة أولى", callback_data="year1")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        f"🎓 أهلاً بيك يا *{user_first_name}* في بوت Modern Academy — Computer Science!\n\n"
        "هتلاقي هنا كل الماتريال والفيديوهات لكل سنة 💪\n"
        "اختار سنتك الدراسية 👇"
    )

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# 🧑‍💻 التعامل مع القوائم
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "year1":
        keyboard = [
            [InlineKeyboardButton("📘 الترم الأول", callback_data="term1_year1")]
        ]
        await query.edit_message_text(
            text="📚 اختار الترم الدراسي 👇", reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "term1_year1":
        keyboard = [
            [InlineKeyboardButton("📗 Introduction to IS", callback_data="is")],
            [InlineKeyboardButton("💻 Computer Programming", callback_data="cp")],
            [InlineKeyboardButton("🧠 Introduction to CS", callback_data="cs")],
            [InlineKeyboardButton("💼 Business", callback_data="bus")],
            [InlineKeyboardButton("⚛️ Physics", callback_data="phy")],
            [InlineKeyboardButton("📐 Calculus", callback_data="calc")],
        ]
        await query.edit_message_text(
            text="🎯 اختر المادة اللي عايز تشوفها 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # 💼 Business
    elif query.data == "bus":
        await send_material(
            query, "💼 Business",
            "https://drive.google.com/drive/folders/1ItwOAslWfqnww4HbvEYCPYdtUmQQAeIO",
            None
        )

    # 📐 Calculus
    elif query.data == "calc":
        await send_material(
            query, "📐 Calculus",
            "https://drive.google.com/drive/folders/1XB0d3pwexTxHrxKT-pRAkvs9Ll6bFP0G",
            "https://www.youtube.com/watch?v=K4PSaQ_LCNQ&list=PLZEjCjHzGS_a5qUPC6upncagEJm8bPS1I"
        )

    # 💻 Computer Programming
    elif query.data == "cp":
        await send_material(
            query, "💻 Computer Programming",
            "https://drive.google.com/drive/folders/1TwRwM0oU5B3-5WMbrE6nh2BlbeHmvlnB",
            "https://www.youtube.com/watch?v=LrR5ha0Frto&list=PLZEjCjHzGS_ZDMHEfoyXYzwjoKzwSNnBp"
        )

    # 🧠 Intro to CS
    elif query.data == "cs":
        await send_material(
            query, "🧠 Introduction to CS",
            "https://drive.google.com/drive/folders/1tBBdJcEncQSWz5B-IZpXQK1GiWfAlLWM",
            None
        )

    # 📗 Intro to IS
    elif query.data == "is":
        await send_material(
            query, "📗 Introduction to IS",
            "https://drive.google.com/drive/folders/1hcBmLxhqE1uobzP8uqP4S6SOw_EWyCLL",
            "https://www.youtube.com/watch?v=2SbkwLO7Wao&list=PL1DUmTEdeA6LXpHtaTyRBok5XnpNzRIfA"
        )

    # ⚛️ Physics
    elif query.data == "phy":
        await send_material(
            query, "⚛️ Physics",
            "https://drive.google.com/drive/folders/1X6QPjkcIoAhcQ7QkMycXnmkCWn9DboJr",
            "https://www.youtube.com/watch?v=hnds6pTG2rs&list=PLZEjCjHzGS_YM2s7B5RQxr4i6vTLXd5Ag"
        )

# 📦 دالة إرسال المادة
async def send_material(query, title, drive_link, video_link):
    keyboard = []
    if drive_link:
        keyboard.append([InlineKeyboardButton("📚 الماتريال", url=drive_link)])
    if video_link:
        keyboard.append([InlineKeyboardButton("🎥 فيديوهات الشرح", url=video_link)])

    keyboard.append([InlineKeyboardButton("⬅️ رجوع", callback_data="term1_year1")])

    await query.edit_message_text(
        text=f"{title}\n\nاختار اللي عايز تشوفه 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

    # 💬 رسالة ختامية بسيطة
    await query.message.reply_text("💬 متنساش تدعيلنا دعوة حلوة ❤️")

# 🚀 تشغيل البوت
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))

    print("🤖 البوت شغال... استمتع يا ماندو!")
    app.run_polling()

if __name__ == "__main__":
    main()
