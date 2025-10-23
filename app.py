from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import requests
import urllib.parse
import os
import logging # লগিং এর জন্য নতুন ইম্পোর্ট

# আপনার লগিং সেটআপ করুন
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ===============================
#          ⚙️ সেটিংস ⚙️
# ===============================
BOT_TOKEN = "8297848554:AAHVX8--wtbap_NEC4bIyjKReJ8b4Z7ebgU"
PRIVATE_CHANNEL_ID = "-1002172050092"  # প্রাইভেট চ্যানেলের ID
PUBLIC_CHANNEL_ID = "https://t.me/shadow_joker_cyberteamhelp"    # পাবলিক চ্যানেলের ইউজারনেম (@ সহ)
PRIVATE_INVITE = "https://t.me/+DLEo8TQ1PjIzYzFl" # প্রাইভেট চ্যানেলের ইনভাইট লিংক
PUBLIC_LINK = "https://t.me/shadow_joker_cyberteamhelp" # পাবলিক চ্যানেলের লিংক
OWNER_ID = 6484972504 # 🤖 মালিকের ইউজার ID (আপনার আইডি দিন)

# AI API এন্ডপয়েন্ট (যদি পরিবর্তন করতে চান)
VIDEO_API_URL = "https://api.yabes-desu.workers.dev/ai/tool/txt2video"
IMAGE_API_URL = "https://text2img.hideme.eu.org/image"

# ===============================
#   /start কমান্ড
# ===============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    keyboard = [
        [InlineKeyboardButton("✅ যাচাই করুন", callback_data="verify")],
        [InlineKeyboardButton("🤖 About Bot", callback_data="about")], # নতুন About বাটন
        [InlineKeyboardButton("👥 আমাদের গ্রুপে যোগ দিন", url=PUBLIC_LINK)] # টেলিগ্রাম গ্রুপ জয়েন বাটন
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # বাংলা এবং ইমোজি সহ উন্নত /start মেসেজ
    await update.message.reply_html(
        f"""
🎉 <b>স্বাগতম, {user.first_name}!</b>

⚠️ এই বটটি ব্যবহার করার আগে আপনাকে অবশ্যই আমাদের দুটি চ্যানেলে যোগ দিতে হবে:

1️⃣ <a href="{PUBLIC_LINK}">পাবলিক চ্যানেলে যোগ দিন</a>  
2️⃣ <a href="{PRIVATE_INVITE}">প্রাইভেট চ্যানেলে যোগ দিন</a>  

উভয় চ্যানেলে যোগ দেওয়ার পর নিচে <b>✅ যাচাই করুন</b> বাটনে ক্লিক করুন।
""",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )


# ===============================
#   ✅ যাচাই বাটন হ্যান্ডলার
# ===============================
async def verify_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user

    # যাচাই করার সময় একটি লোডিং উত্তর দিন
    await query.answer("⌛ চ্যানেল সদস্যতা যাচাই করা হচ্ছে...", show_alert=False)

    try:
        # get_chat_member অ্যাসিঙ্ক্রোনাস ফাংশন, তাই await ব্যবহার করা হয়েছে
        private_member = await context.bot.get_chat_member(PRIVATE_CHANNEL_ID, user.id)
        public_member = await context.bot.get_chat_member(PUBLIC_CHANNEL_ID, user.id)

        # সদস্যতার স্থিতি যাচাই
        if (
            private_member.status in ["member", "administrator", "creator"]
            and public_member.status in ["member", "administrator", "creator"]
        ):
            # যাচাই সফল হলে মেসেজ এডিট করুন
            await query.message.edit_text(
                f"""
✅ <b>যাচাই সফল!</b>

স্বাগতম {user.first_name} 🥳  
আপনি এখন নিচের কমান্ডগুলো ব্যবহার করতে পারেন:

🎥 <code>/vid আপনার বর্ণনা</code> → AI ভিডিও তৈরি করুন  
🖼️ <code>/flux আপনার বর্ণনা</code> → AI ছবি (Image) তৈরি করুন  

👑 <b>মালিক:</b> <a href="tg://user?id={OWNER_ID}">আমার মালিক</a>
🛠️ <b>তৈরি করেছেন:</b> <a href="https://t.me/code_predator_acs">Code Predator</a>
                """,
                parse_mode="HTML"
            )
        else:
            # যাচাই ব্যর্থ হলে সতর্কতা মেসেজ দিন
            await query.answer("❌ আপনাকে অবশ্যই প্রথমে উভয় চ্যানেলে যোগ দিতে হবে!", show_alert=True)

    except Exception:
        # কোনো ত্রুটি হলে (যেমন: প্রাইভেট চ্যানেলের ID ভুল হলে)
        await query.answer("❌ যাচাইয়ে সমস্যা হয়েছে, চ্যানেলের ID ঠিক আছে কিনা দেখুন!", show_alert=True)
        logging.error(f"যাচাই ত্রুটি: {user.id} চ্যানেলের সদস্যতা যাচাই করতে পারেনি।")

# ===============================
#   🤖 About Bot বাটন হ্যান্ডলার
# ===============================
async def about_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    # মূল মেনুতে ফিরে যাওয়ার বাটন
    keyboard = [
        [InlineKeyboardButton("⬅️ ব্যাক", callback_data="start_menu")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text(
        f"""
🌟 <b>SHADOW  AI Bot সম্পর্কে:</b>

এই বটটি শক্তিশালী AI মডেল ব্যবহার করে টেক্সট প্রম্পট থেকে দুর্দান্ত ভিডিও এবং ছবি তৈরি করতে পারে।

- <b>ভিডিও মডেল:</b> Sora-এর মতো (API দ্বারা প্রোভাইড করা)
- <b>ছবি মডেল:</b> Flux

অনুগ্রহ করে শালীন এবং সঠিক প্রম্পট ব্যবহার করুন।
কোনো সমস্যা হলে মালিকের সাথে যোগাযোগ করুন।

👑 <b>মালিক:</b> <a href="tg://user?id={OWNER_ID}">আমার মালিক</a>
🛠️ <b>তৈরি করেছেন:</b> <a href="https://t.me/code_predator_acs">Code Predator</a>
""",
        parse_mode="HTML",
        reply_markup=reply_markup
    )

# ===============================
#   ⬅️ ব্যাক বাটন হ্যান্ডলার (মূল মেনু)
# ===============================
async def back_to_start_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    
    # /start ফাংশনের যুক্তি পুনরায় ব্যবহার করুন
    keyboard = [
        [InlineKeyboardButton("✅ যাচাই করুন", callback_data="verify")],
        [InlineKeyboardButton("🤖 About Bot", callback_data="about")],
        [InlineKeyboardButton("👥 আমাদের গ্রুপে যোগ দিন", url=PUBLIC_LINK)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text(
        f"""
🎉 <b>স্বাগতম, {user.first_name}!</b>

⚠️ এই বটটি ব্যবহার করার আগে আপনাকে অবশ্যই আমাদের দুটি চ্যানেলে যোগ দিতে হবে:

1️⃣ <a href="{PUBLIC_LINK}">পাবলিক চ্যানেলে যোগ দিন</a>  
2️⃣ <a href="{PRIVATE_INVITE}">প্রাইভেট চ্যানেলে যোগ দিন</a>  

উভয় চ্যানেলে যোগ দেওয়ার পর নিচে <b>✅ যাচাই করুন</b> বাটনে ক্লিক করুন।
""",
        reply_markup=reply_markup,
        parse_mode="HTML",
        disable_web_page_preview=True
    )


# ===============================
#   🎥 AI টেক্সট থেকে ভিডিও কমান্ড (/vid)
# ===============================
async def vid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_html("""
❌ <b>ভিডিও প্রম্পট দিন!</b>

আপনি যে ভিডিওটি তৈরি করতে চান তার একটি বর্ণনা দিতে হবে।
<b>উদাহরণ:</b> <code>/vid মাঠে দৌড়াচ্ছে একটি ঘোড়া</code>
""")
        return

    prompt = " ".join(context.args)
    chat_id = update.message.chat_id
    user = update.message.from_user

    generating = await update.message.reply_html("⏳ <i>আপনার ভিডিও তৈরি হচ্ছে, অপেক্ষা করুন...</i>")
    await context.bot.send_chat_action(chat_id=chat_id, action="upload_video")

    try:
        encoded_prompt = urllib.parse.quote(prompt)
        api_url = f"{VIDEO_API_URL}?prompt={encoded_prompt}"

        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        if data.get("success"):
            video_url = data.get("url")
            caption = f"""
✅ <b>তৈরি সম্পন্ন!</b>

👤 <b>জন্য:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>
💡 <b>মডেল:</b> Sora-like
📝 <b>প্রম্পট:</b> {prompt}
🚀 <b>অবস্থা:</b> সফলভাবে তৈরি হয়েছে!

🛠️ <b>তৈরি করেছেন:</b> <a href="t.me/SHADOW_JOKER_CTH">SHADOW JOKER</a>
"""
            await context.bot.send_video(
                chat_id=chat_id,
                video=video_url,
                caption=caption,
                parse_mode="HTML",
                reply_to_message_id=update.message.message_id
            )
            # জেনারেটিং মেসেজটি ডিলিট করুন
            await context.bot.delete_message(chat_id=chat_id, message_id=generating.message_id)
        else:
            await generating.edit_text("❌ <b>ভিডিও তৈরি ব্যর্থ!</b>\n\nঅনুগ্রহ করে আবার চেষ্টা করুন।", parse_mode="HTML")

    except Exception as e:
        logging.error(f"ভিডিও তৈরির API ত্রুটি: {e}")
        await generating.edit_text(f"❌ <b>একটি ত্রুটি হয়েছে!</b>\n\n<i>বিস্তারিত:</i> {e}", parse_mode="HTML")


# ===============================
#   🖼️ AI টেক্সট থেকে ছবি কমান্ড (/flux)
# ===============================
async def flux(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_html("❌ <b>ছবি প্রম্পট দিন!</b>\n\nদয়া করে /flux কমান্ডের পরে একটি বর্ণনা লিখুন।")
        return

    prompt = " ".join(context.args)
    chat_id = update.message.chat_id
    user = update.message.from_user

    generating = await update.message.reply_html("⏳ <i>আপনার ছবি তৈরি হচ্ছে, অপেক্ষা করুন...</i>")
    await context.bot.send_chat_action(chat_id=chat_id, action="upload_photo")

    try:
        encoded_prompt = urllib.parse.quote(prompt)
        # ছবির জন্য API কল
        api_url = f"{IMAGE_API_URL}?prompt={encoded_prompt}&model=flux"

        response = requests.get(api_url)
        response.raise_for_status() # HTTP ত্রুটি হলে Exception দেখাবে

        if response.status_code == 200:
            caption = f"""<b>✅ তৈরি সম্পন্ন!</b>

👤 <b>জন্য:</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>
💡 <b>মডেল:</b> Flux
📝 <b>প্রম্পট:</b> {prompt}
🚀 <b>অবস্থা:</b> সফলভাবে তৈরি হয়েছে!

🛠️ <b>তৈরি করেছেন:</b> <a href="https://t.me/code_predator_acs">Code Predator</a>
"""
            # বাইনারি কন্টেন্ট সরাসরি send_photo তে পাঠান
            await context.bot.send_photo(
                chat_id=chat_id,
                photo=response.content,
                caption=caption,
                parse_mode="HTML",
                reply_to_message_id=update.message.message_id
            )
            # জেনারেটিং মেসেজটি ডিলিট করুন
            await context.bot.delete_message(chat_id=chat_id, message_id=generating.message_id)
        else:
            await generating.edit_text(f"❌ ছবি তৈরি ব্যর্থ হলো (স্থিতি কোড: {response.status_code})। আবার চেষ্টা করুন।", parse_mode="HTML")

    except Exception as e:
        logging.error(f"ছবি তৈরির API ত্রুটি: {e}")
        await generating.edit_text(f"❌ ছবি তৈরির সময় একটি ত্রুটি হয়েছে।\n\n{e}", parse_mode="HTML")


# ===============================
#        🚀 মেইন ফাংশন 🚀
# ===============================
def main():
    # ApplicationBuilder ব্যবহার করে বট তৈরি করুন
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # কমান্ড হ্যান্ডলার যোগ করুন
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("vid", vid))
    app.add_handler(CommandHandler("flux", flux))
    
    # CallbackQuery হ্যান্ডলার যোগ করুন (বাটন ক্লিকের জন্য)
    app.add_handler(CallbackQueryHandler(verify_callback, pattern="verify"))
    app.add_handler(CallbackQueryHandler(about_callback, pattern="about")) # About বাটন হ্যান্ডলার
    app.add_handler(CallbackQueryHandler(back_to_start_menu, pattern="start_menu")) # ব্যাক বাটন হ্যান্ডলার

    print("✅ Predator AI Bot চালু হয়েছে...")
    
    # বট পোলিং শুরু করুন
    app.run_polling()


if __name__ == "__main__":
    main()