import requests
import base64
import re

# لینک منبع اصلی (v2rayCrow)
source_url = "https://raw.githubusercontent.com/v2rayCrow/Sub-Link-Output/main/sub.txt"

# فایل خروجی در همین ریپو
output_file = "sub.txt"

def main():
    # دانلود داده‌ها از منبع اصلی
    data = requests.get(source_url).text.strip()

    # تلاش برای decode از base64
    try:
        decoded = base64.b64decode(data).decode("utf-8")
    except Exception:
        decoded = data

    links = [line.strip() for line in decoded.splitlines() if line.strip()]

    new_links = []
    for i, link in enumerate(links, start=1):
        # حذف هر اسم قدیمی بعد از #
        link = re.sub(r'#.*', '', link)

        # اضافه کردن نام جدید (برای همه پروتکل‌ها)
        if '#' not in link:
            link += f"#Rafati%20Capital%20{i}"
        else:
            link = re.sub(r'#.*', f"#Rafati%20Capital%20{i}", link)

        new_links.append(link)

    # دوباره به base64 برگردان
    encoded = base64.b64encode("\n".join(new_links).encode()).decode()

    with open(output_file, "w") as f:
        f.write(encoded)

    print("✅ Subscription updated successfully!")

if __name__ == "__main__":
    main()
