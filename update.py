import requests
import base64
import re

# لینک منبع اصلی (v2rayCrow)
source_url = "https://raw.githubusercontent.com/v2rayCrow/Sub-Link-Output/main/sub.txt"

# فایل خروجی (در همین ریپو)
output_file = "sub.txt"

def main():
    # دانلود محتوای منبع
    data = requests.get(source_url).text.strip()

    # دیکد از base64
    try:
        decoded = base64.b64decode(data).decode("utf-8")
    except Exception:
        decoded = data

    # تقسیم لینک‌ها
    links = [line for line in decoded.splitlines() if line.strip()]

    # تغییر نام سرورها
    new_links = []
    for i, link in enumerate(links, start=1):
        # جایگزینی نام سرور
        link = re.sub(r'(#|%23)[^?]+', '', link)  # حذف اسم قبلی
        if '?' in link:
            link += f"&remarks=Rafati%20Capital%20{i}"
        else:
            link += f"#Rafati%20Capital%20{i}"
        new_links.append(link)

    # انکد مجدد به base64
    encoded = base64.b64encode("\n".join(new_links).encode()).decode()

    # ذخیره در فایل
    with open(output_file, "w") as f:
        f.write(encoded)

    print("✅ Subscription updated successfully!")

if __name__ == "__main__":
    main()
