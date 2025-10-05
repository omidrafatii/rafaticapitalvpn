import requests
import base64
import re
import random
import urllib.parse
from collections import OrderedDict

# ====== تنظیمات ======
# لیست منابع (هر URL که محتواشون مشابه subscription باشه)
sources = [
    "https://raw.githubusercontent.com/v2rayCrow/Sub-Link-Output/main/sub.txt",
    # "https://raw.githubusercontent.com/other/source1/main/sub.txt",
    # "https://example.com/another-sub.txt",
]

# اسم سایت برای تبلیغ
site_name = "rafaticapital.ir"

# فایل خروجی داخل ریپو
output_file = "sub.txt"

# حداکثر تعداد سرور در خروجی (None برای نامحدود)
MAX_SERVERS = None  # یا مثلاً 200

# لیست پرچم‌ها (ایموجی) — هر کدوم خواستی اضافه/حذف کن
flags = [
    "🇮🇷","🇺🇸","🇬🇧","🇩🇪","🇫🇷","🇨🇦","🇦🇺","🇯🇵","🇰🇷","🇮🇳",
    "🇷🇺","🇦🇪","🇸🇬","🇳🇱","🇨🇭","🇸🇪","🇳🇴","🇪🇸","🇮🇹","🇧🇷"
]
# =====================

def fetch_source(url):
    try:
        r = requests.get(url, timeout=20)
        r.raise_for_status()
        return r.text.strip()
    except Exception as e:
        print(f"⚠️ Failed to fetch {url}: {e}")
        return ""

def decode_maybe_base64(data):
    # اگر کل داده base64 انکُد شده باشه دیکد کن، در غیر این صورت برگردان همون متن
    data = data.strip()
    if not data:
        return ""
    # heuristic: اگر فقط شامل حروف base64 و طول مناسب بود، تلاش کن
    try:
        decoded = base64.b64decode(data).decode("utf-8")
        # اگر بعد از دیکد شدن لاین‌های لینک داشت، برگردون
        if "\n" in decoded or "://" in decoded:
            return decoded
    except Exception:
        pass
    return data

def normalize_and_split(data):
    lines = []
    for line in data.splitlines():
        s = line.strip()
        if s:
            lines.append(s)
    return lines

def unique_preserve_order(seq):
    # حذف تکراری‌ها
    return list(OrderedDict.fromkeys(seq))

def add_remarks_and_flags(links):
    new_links = []
    for i, link in enumerate(links, start=1):
        # حذف هر remark قدیمی (بعد از #) تا جایگزین کنیم
        link = re.sub(r'#.*', '', link)

        # یک پرچم تصادفی بردار
        flag = random.choice(flags)

        # متن remark که می‌خواهیم نمایش بدیم
        remark_text = f"Rafati Capital {i} - {site_name} {flag}"

        # percent-encode برای ایمن بودن
        encoded_remark = urllib.parse.quote(remark_text, safe='')

        # اضافه کردن remark به انتهای لینک با #
        link_with_remark = f"{link}#{encoded_remark}"

        new_links.append(link_with_remark)
    return new_links

def main():
    all_links = []
    for src in sources:
        raw = fetch_source(src)
        if not raw:
            continue
        decoded = decode_maybe_base64(raw)
        lines = normalize_and_split(decoded)
        all_links.extend(lines)

    # یکتا کردن و حفظ ترتیب
    all_links = unique_preserve_order(all_links)

    # می‌تونی اینجا shuffle کنی اگر می‌خواهی ترتیب رندوم باشه
    random.shuffle(all_links)

    # محدود کردن تعداد اگر خواستی
    if MAX_SERVERS:
        all_links = all_links[:MAX_SERVERS]

    # اضافه کردن remarks و flags
    new_links = add_remarks_and_flags(all_links)

    # انکد مجدد به base64 برای خروجی
    encoded = base64.b64encode("\n".join(new_links).encode()).decode()

    with open(output_file, "w") as f:
        f.write(encoded)

    print(f"✅ Updated {len(new_links)} servers into {output_file}")

if __name__ == "__main__":
    main()
