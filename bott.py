from keep_alive import keep_alive
keep_alive()

import asyncio
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ContextTypes, filters
)

# ✨ التوكن
TOKEN = "8587194106:AAHXquYldB0-oRc_nqsqDy0CuocrHSAeQqQ"

# 🧑‍💻 معرف المطور (هات ID بتاعك من @userinfobot)
DEVELOPER_ID = 1379876091  # ← غيّر الرقم ده بـ Telegram ID بتاعك

# 🎓 رسالة البداية
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_first_name = update.effective_user.first_name
    keyboard = [
        [InlineKeyboardButton("🧑‍💻 سنة أولى", callback_data="year1")],
        [InlineKeyboardButton("💬 تواصل مع المطور", callback_data="contact")],
        [InlineKeyboardButton("💡 إرسال اقتراح", callback_data="suggestion")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        f"🎓 أهلاً بيك يا *{user_first_name}* في بوت Modern Academy — Computer Science!\n\n"
        "هتلاقي هنا كل الماتريال والفيديوهات لكل سنة 💪\n"
        "اختار سنتك الدراسية أو تواصل معانا 👇"
    )

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

# ⚙️ التعامل مع القوائم
async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # --- القائمة الرئيسية ---
    if query.data == "year1":
        keyboard = [
            [InlineKeyboardButton("📘 الترم الأول", callback_data="term1_year1")],
            [InlineKeyboardButton("⬅️ رجوع", callback_data="main_menu")]
        ]
        await query.edit_message_text(
            text="📚 اختار الترم الدراسي 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "term1_year1":
        keyboard = [
            [InlineKeyboardButton("📗 Introduction to IS", callback_data="is")],
            [InlineKeyboardButton("💻 Computer Programming", callback_data="cp")],
            [InlineKeyboardButton("🧠 Introduction to CS", callback_data="cs")],
            [InlineKeyboardButton("💼 Business", callback_data="bus")],
            [InlineKeyboardButton("⚛️ Physics", callback_data="phy")],
            [InlineKeyboardButton("📐 Calculus", callback_data="calc")],
            [InlineKeyboardButton("⬅️ رجوع", callback_data="year1")]
        ]
        await query.edit_message_text(
            text="🎯 اختر المادة اللي عايز تشوفها 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # --- التواصل مع المطور ---
    elif query.data == "contact":
        keyboard = [
            [InlineKeyboardButton("📞 واتساب", url="https://wa.me/201126874664")],
            [InlineKeyboardButton("💬 تيلجرام", url="https://t.me/moaz_samir")],
            [InlineKeyboardButton("⬅️ رجوع", callback_data="main_menu")]
        ]
        await query.edit_message_text(
            text="📬 تقدر تتواصل مع المطور عن طريق:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # --- إرسال اقتراح ---
    elif query.data == "suggestion":
        await query.edit_message_text("💡 اكتب اقتراحك أو التعديل اللي في بالك، وأنا هوصله للمطور 👇")
        context.user_data["awaiting_suggestion"] = True

    # --- رجوع للقائمة الرئيسية ---
    elif query.data == "main_menu":
        await start(query, context)

    # --- المواد ---
    elif query.data in ["bus", "calc", "cp", "cs", "is", "phy"]:
        materials = {
            "bus": ("💼 Business", "https://drive.google.com/drive/folders/1ItwOAslWfqnww4HbvEYCPYdtUmQQAeIO", None),
            "calc": ("📐 Calculus", "https://drive.google.com/drive/folders/1XB0d3pwexTxHrxKT-pRAkvs9Ll6bFP0G",
                     "https://www.youtube.com/watch?v=K4PSaQ_LCNQ&list=PLZEjCjHzGS_a5qUPC6upncagEJm8bPS1I"),
            "cp": ("💻 Computer Programming", "https://drive.google.com/drive/folders/1TwRwM0oU5B3-5WMbrE6nh2BlbeHmvlnB",
                   "https://www.youtube.com/watch?v=LrR5ha0Frto&list=PLZEjCjHzGS_ZDMHEfoyXYzwjoKzwSNnBp"),
            "cs": ("🧠 Introduction to CS", "https://drive.google.com/drive/folders/1tBBdJcEncQSWz5B-IZpXQK1GiWfAlLWM", None),
            "is": ("📗 Introduction to IS", "https://drive.google.com/drive/folders/1hcBmLxhqE1uobzP8uqP4S6SOw_EWyCLL",
                   "https://www.youtube.com/watch?v=2SbkwLO7Wao&list=PL1DUmTEdeA6LXpHtaTyRBok5XnpNzRIfA"),
            "phy": ("⚛️ Physics", "https://drive.google.com/drive/folders/1X6QPjkcIoAhcQ7QkMycXnmkCWn9DboJr",
                    "https://www.youtube.com/watch?v=hnds6pTG2rs&list=PLZEjCjHzGS_YM2s7B5RQxr4i6vTLXd5Ag")
        }
        title, drive, video = materials[query.data]
        await send_material(query, title, drive, video)

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

    await query.message.reply_text("💬 متنساش تدعيلنا دعوة حلوة ❤️")

# 📨 استقبال الاقتراحات من المستخدمين
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("awaiting_suggestion"):
        suggestion = update.message.text
        user = update.effective_user
        await update.message.reply_text("✅ تم إرسال اقتراحك بنجاح! شكراً لمشاركتك ❤️")

        # إرسال الاقتراح للمطور
        await context.bot.send_message(
            chat_id=DEVELOPER_ID,
            text=f"📩 اقتراح جديد من {user.first_name} (@{user.username}):\n\n{suggestion}"
        )

        context.user_data["awaiting_suggestion"] = False

# 🚀 تشغيل البوت
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))

    print("🤖 البوت شغال... استمتع يا ماندو!")
    app.run_polling()

if __name__ == "__main__":
    main()
