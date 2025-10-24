from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
import urllib.parse
import os
import logging

# ===============================
# 🔰 LOGGING সেটআপ
# ===============================
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# ===============================
# ⚙️ বট সেটিংস ⚙️
# ===============================
BOT_TOKEN = "8297848554:AAHVX8--wtbap_NEC4bIyjKReJ8b4Z7ebgU"

PRIVATE_CHANNEL_ID = "-1002172050092"
PUBLIC_CHANNEL_ID = "@shadow_joker_cyberteamhelp"
PRIVATE_INVITE = "https://t.me/+DLEo8TQ1PjIzYzFl"
PUBLIC_LINK = "https://t.me/SHADOW_JOKER_CTH"

OWNER_ID = 6484972504

VIDEO_API_URL = "https://api.yabes-desu.workers.dev/ai/tool/txt2video"
IMAGE_API_URL = "https://text2img.hideme.eu.org/image"

# ===============================
# 🏁 /start কমান্ড
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    keyboard = [
        [InlineKeyboardButton("✅ যাচাই করুন", callback_data="verify")],
        [InlineKeyboardButton("🤖 About Bot", callback_data="about")],
        [InlineKeyboardButton("👥 আমাদের গ্রুপে যোগ দিন", url=PUBLIC_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_html(
        f"""
🎉 <b>স্বাগতম, {user.first_name}!</b>

⚠️ এই বটটি ব্যবহার করার আগে আপনাকে অবশ্যই আমাদের দুটি চ্যানেলে যোগ দিতে হবে:

1️⃣ পাবলিক চ্যানেলে যোগ দিন  
2️⃣ প্রাইভেট চ্যানেলে যোগ দিন  

উভয় চ্যানেলে যোগ দেওয়ার পর নিচে <b>✅ যাচাই করুন</b> বাটনে ক্লিক করুন।
""",
        reply_markup=reply_markup,
        disable_web_page_preview=True,
    )

# ===============================
# ✅ যাচাই বাটন
# ===============================
async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer("⌛ চ্যানেল যাচাই হচ্ছে...", show_alert=False)

    try:
        private_member = await context.bot.get_chat_member(PRIVATE_CHANNEL_ID, user.id)
        public_member = await context.bot.get_chat_member(PUBLIC_CHANNEL_ID, user.id)

        if (
            private_member.status in ["member", "administrator", "creator"]
            and public_member.status in ["member", "administrator", "creator"]
        ):
            await query.message.edit_text(
                f"""
✅ <b>যাচাই সফল!</b>

স্বাগতম {user.first_name} 🥳  

আপনি এখন নিচের কমান্ডগুলো ব্যবহার করতে পারেন:

🎥 <code>/vid</code> আপনার টেক্সট → ভিডিও তৈরি  
🖼️ <code>/flux</code> আপনার টেক্সট → ছবি তৈরি  

👑 <b>মালিক:</b> SHADOW JOKER  
🔗 <a href="{PUBLIC_LINK}">t.me/SHADOW_JOKER_CTH</a>
""",
                parse_mode="HTML",
            )
        else:
            await query.answer("❌ আপনাকে অবশ্যই উভয় চ্যানেলে যোগ দিতে হবে!", show_alert=True)
    except Exception as e:
        logging.error(f"চ্যানেল যাচাই ত্রুটি: {e}")
        await query.answer("❌ যাচাই ব্যর্থ! চ্যানেল ID সঠিক আছে কিনা দেখুন।", show_alert=True)

# ===============================
# 🤖 About Bot
# ===============================
async def about_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    keyboard = [[InlineKeyboardButton("⬅️ ব্যাক", callback_data="start_menu")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text(
        f"""
🌟 <b>SHADOW BOT সম্পর্কে:</b>

এই বটটি AI মডেল ব্যবহার করে টেক্সট প্রম্পট থেকে দুর্দান্ত ভিডিও এবং ছবি তৈরি করতে পারে।

🎥 <b>ভিডিও মডেল:</b> Sora-like  
🖼️ <b>ছবি মডেল:</b> Flux  

👑 <b>মালিক:</b> SHADOW JOKER  
🔗 <a href="{PUBLIC_LINK}">t.me/SHADOW_JOKER_CTH</a>
""",
        parse_mode="HTML",
        reply_markup=reply_markup,
    )

# ===============================
# 🔙 ব্যাক টু স্টার্ট
# ===============================
async def back_to_start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    keyboard = [
        [InlineKeyboardButton("✅ যাচাই করুন", callback_data="verify")],
        [InlineKeyboardButton("🤖 About Bot", callback_data="about")],
        [InlineKeyboardButton("👥 আমাদের গ্রুপে যোগ দিন", url=PUBLIC_LINK)],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.edit_text(
        f"""
🎉 <b>স্বাগতম, {user.first_name}!</b>

⚠️ আমাদের পাবলিক এবং প্রাইভেট চ্যানেলে যোগ দিন,
তারপর নিচের <b>✅ যাচাই করুন</b> বাটনে ক্লিক করুন।
""",
        reply_markup=reply_markup,
        parse_mode="HTML",
        disable_web_page_preview=True,
    )

# ===============================
# 🎥 ভিডিও কমান্ড
# ===============================
async def vid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_html(
            "❌ <b>ভিডিও প্রম্পট দিন!</b>\n\nউদাহরণ:\n<code>/vid মাঠে দৌড়াচ্ছে একটি ঘোড়া</code>"
        )
        return

    prompt = " ".join(context.args)
    chat_id = update.message.chat_id
    user = update.message.from_user
    generating = await update.message.reply_html("⏳ <i>ভিডিও তৈরি হচ্ছে...</i>")
    await context.bot.send_chat_action(chat_id=chat_id, action="upload_video")

    try:
        encoded_prompt = urllib.parse.quote(prompt)
        api_url = f"{VIDEO_API_URL}?prompt={encoded_prompt}"
        response = requests.get(api_url)
        data = response.json()

        if data.get("success"):
            video_url = data.get("url")
            caption = f"""
✅ <b>ভিডিও তৈরি সম্পন্ন!</b>

👤 <b>ব্যবহারকারী:</b> {user.first_name}  
📝 <b>প্রম্পট:</b> {prompt}  
🛠️ <b>তৈরি করেছেন:</b> SHADOW JOKER  
🔗 <a href="{PUBLIC_LINK}">t.me/SHADOW_JOKER_CTH</a>
"""
            await context.bot.send_video(
                chat_id=chat_id,
                video=video_url,
                caption=caption,
                parse_mode="HTML",
            )
            await context.bot.delete_message(chat_id=chat_id, message_id=generating.message_id)
        else:
            await generating.edit_text("❌ ভিডিও তৈরি ব্যর্থ!", parse_mode="HTML")
    except Exception as e:
        logging.error(f"ভিডিও API ত্রুটি: {e}")
        await generating.edit_text(f"❌ ত্রুটি: {e}", parse_mode="HTML")

# ===============================
# 🖼️ ছবি কমান্ড
# ===============================
async def flux(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_html("❌ <b>ছবি প্রম্পট দিন!</b>\n\nউদাহরণ:\n<code>/flux একটি সুন্দর শহর</code>")
        return

    prompt = " ".join(context.args)
    chat_id = update.message.chat_id
    user = update.message.from_user
    generating = await update.message.reply_html("⏳ <i>ছবি তৈরি হচ্ছে...</i>")
    await context.bot.send_chat_action(chat_id=chat_id, action="upload_photo")

    try:
        encoded_prompt = urllib.parse.quote(prompt)
        api_url = f"{IMAGE_API_URL}?prompt={encoded_prompt}&model=flux"
        response = requests.get(api_url)

        if response.status_code == 200:
            caption = f"""
✅ <b>ছবি তৈরি সম্পন্ন!</b>

👤 <b>ব্যবহারকারী:</b> {user.first_name}  
📝 <b>প্রম্পট:</b> {prompt}  
🛠️ <b>তৈরি করেছেন:</b> SHADOW JOKER  
🔗 <a href="{PUBLIC_LINK}">t.me/SHADOW_JOKER_CTH</a>
"""
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=response.content,
                caption=caption,
                parse_mode="HTML",
            )
            await context.bot.delete_message(chat_id=chat_id, message_id=generating.message_id)
        else:
            await generating.edit_text("❌ ছবি তৈরি ব্যর্থ!", parse_mode="HTML")
    except Exception as e:
        logging.error(f"ছবি API ত্রুটি: {e}")
        await generating.edit_text(f"❌ ত্রুটি: {e}", parse_mode="HTML")

# ===============================
# 🚀 MAIN FUNCTION
# ===============================
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vid", vid))
    app.add_handler(CommandHandler("flux", flux))

    app.add_handler(CallbackQueryHandler(verify_callback, pattern="verify"))
    app.add_handler(CallbackQueryHandler(about_callback, pattern="about"))
    app.add_handler(CallbackQueryHandler(back_to_start_menu, pattern="start_menu"))

    print("✅ SHADOW BOT চালু হয়েছে...")
    app.run_polling()

if __name__ == "__main__":
    main()
