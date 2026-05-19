from telethon import TelegramClient
from telethon.errors import FloodWaitError, UserPrivacyRestrictedError
import schedule
import asyncio
from dotenv import load_dotenv
import os
import time
from datetime import datetime
load_dotenv()


API_ID = os.getenv("API_ID")
API_HASH =  os.getenv("API_HASH")
SESSION_NAME = "userbot_session"

TARGETS = [
    "@vwhoami",
]

MESSAGES = [
    "Xayrli tong! ☀️ Bugun ham ajoyib kun bo'lsin!",
    "Salom! Bugun qanday ahvolsiz? 😊",
    "Assalomu alaykum! Bugun maqsadlaringizga erishishingizni tilayman 🎯",
]

BIRTHDAYS = {
    "@vwhoami": "05-19",
}

BIRTHDAY_MESSAGES = [
    "Tug'ilgan kuningiz bilan! 🎉 Sizga baxt va muvaffaqiyat tilayman.",
    "Happy birthday! 🎂 Bugun siz uchun maxsus kun bo'lsin.",
    "Yana bir yil baxt, sog'liq va kulgu bilan kelishini tilayman! 🥳",
]


SCHEDULE_TIMES = [
    "22:24",
]

DELAY_BETWEEN_MESSAGES = 5


import random

client = TelegramClient(SESSION_NAME, API_ID, API_HASH)


async def send_messages():
    """Barcha targetlarga xabar yuboradi"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{now}] Xabar yuborish boshlandi...")

    message = random.choice(BIRTHDAY_MESSAGES)
    success = 0
    failed = 0

    for target in BIRTHDAYS:
        try:
            await client.send_message(target, message)
            print(f"  ✅ {target} ga yuborildi")
            success += 1
            await asyncio.sleep(DELAY_BETWEEN_MESSAGES)

        except FloodWaitError as e:
            print(f"  ⏳ Flood wait: {e.seconds} soniya kutilmoqda...")
            await asyncio.sleep(e.seconds)
            try:
                await client.send_message(target, message)
                print(f"  ✅ {target} ga yuborildi (2-urinish)")
                success += 1
            except Exception as ex:
                print(f"  ❌ {target} — xato: {ex}")
                failed += 1

        except UserPrivacyRestrictedError:
            print(f"  ❌ {target} — foydalanuvchi xabar qabul qilishni cheklagan")
            failed += 1

        except Exception as e:
            print(f"  ❌ {target} — xato: {e}")
            failed += 1

    print(f"\n  📊 Natija: {success} muvaffaqiyatli, {failed} xato")
    print(f"  📝 Yuborilgan xabar: '{message}'")


def parse_birthday(value):
    normalized = value.replace('/', '-').replace('.', '-').strip()
    parts = normalized.split('-')
    if len(parts) == 3:
        month, day = parts[-2], parts[-1]
    elif len(parts) == 2:
        month, day = parts
    else:
        raise ValueError(f"Noto'g'ri tug'ilgan kun formati: {value}")
    return month.zfill(2), day.zfill(2)


async def send_birthday_messages():
    today = datetime.now().strftime("%m-%d")
    birthday_targets = [
        target for target, date in BIRTHDAYS.items()
        if "-".join(parse_birthday(date)) == today
    ]

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{now}] Tug'ilgan kunlari tekshirilmoqda...")

    if not birthday_targets:
        print("  🎂 Bugun tug'ilgan kuni bo'lgan foydalanuvchi yo'q.")
        return

    message = random.choice(BIRTHDAY_MESSAGES)
    success = 0
    failed = 0

    for target in birthday_targets:
        try:
            await client.send_message(target, message)
            print(f"  ✅ {target} ga yuborildi")
            success += 1
            await asyncio.sleep(DELAY_BETWEEN_MESSAGES)

        except FloodWaitError as e:
            print(f"  ⏳ Flood wait: {e.seconds} soniya kutilmoqda...")
            await asyncio.sleep(e.seconds)
            try:
                await client.send_message(target, message)
                print(f"  ✅ {target} ga yuborildi (2-urinish)")
                success += 1
            except Exception as ex:
                print(f"  ❌ {target} — xato: {ex}")
                failed += 1

        except UserPrivacyRestrictedError:
            print(f"  ❌ {target} — foydalanuvchi xabar qabul qilishni cheklagan")
            failed += 1

        except Exception as e:
            print(f"  ❌ {target} — xato: {e}")
            failed += 1

    print(f"\n  📊 Natija: {success} muvaffaqiyatli, {failed} xato")
    print(f"  📝 Tug'ilgan kun xabari: '{message}'")


def schedule_job():
    loop = asyncio.get_event_loop()
    loop.create_task(send_birthday_messages())


async def main():
    print("=" * 50)
    print("  Telegram Userbot ishga tushdi")
    print("=" * 50)

    for t in SCHEDULE_TIMES:
        schedule.every().day.at(t).do(schedule_job)
        print(f"  ⏰ Jadvalga qo'shildi: har kuni soat {t}")

    print(f"\n  👥 Targetlar soni: {len(TARGETS)}")
    print(f"  💬 Tug'ilgan kun xabarlari: {len(BIRTHDAY_MESSAGES)} ta")
    print("\n  Userbot ishlayapti... (to'xtatish uchun Ctrl+C)\n")

    while True:
        schedule.run_pending()
        await asyncio.sleep(30)


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())