import os
from flask import Flask, render_template_string

app = Flask(__name__)

# ==========================================
# 🎨 استایل‌های سایت (CSS)
# ==========================================
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;700;900&display=swap');

:root {
    --bg: #f8fafc;
    --ink: #0f172a;
    --muted: #64748b;
    --primary: #1d4ed8;
    --accent: #06b6d4;
    --gold: #fbbf24;
    --card: #ffffff;
    --line: #e2e8f0;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Vazirmatn', sans-serif; background: var(--bg); color: var(--ink); line-height: 1.8; direction: rtl; }
.container { max-width: 1100px; margin: 0 auto; padding: 0 20px; }

/* Navbar */
.navbar { background: rgba(255,255,255,0.9); backdrop-filter: blur(10px); border-bottom: 1px solid var(--line); position: sticky; top: 0; z-index: 100; }
.nav-inner { display: flex; justify-content: space-between; align-items: center; height: 75px; }
.brand { display: flex; align-items: center; gap: 12px; text-decoration: none; color: var(--ink); }
.logo { width: 45px; height: 45px; background: linear-gradient(135deg, var(--primary), var(--accent)); color: white; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-weight: 900; font-size: 22px; }
.nav-links { display: flex; gap: 8px; }
.nav-links a { text-decoration: none; color: var(--ink); padding: 8px 16px; border-radius: 10px; transition: 0.3s; font-weight: 500; }
.nav-links a:hover, .nav-links a.active { background: var(--primary); color: white; }

/* Hero */
.hero { background: linear-gradient(135deg, #0f172a, #1e3a8a); color: white; padding: 90px 0; border-radius: 0 0 40px 40px; text-align: center; }
.hero h1 { font-size: 40px; margin-bottom: 20px; }
.hero span { color: var(--gold); }
.hero p { font-size: 18px; opacity: 0.9; max-width: 700px; margin: 0 auto 30px; }
.btn { display: inline-block; padding: 12px 28px; border-radius: 12px; background: var(--gold); color: #1c1917; text-decoration: none; font-weight: bold; font-size: 16px; transition: 0.3s; border: none; cursor: pointer; }
.btn:hover { transform: translateY(-3px); box-shadow: 0 10px 20px rgba(251,191,36,0.4); }

/* Sections & Cards */
.section { padding: 70px 0; }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 25px; }
.card { background: var(--card); padding: 30px; border-radius: 20px; border: 1px solid var(--line); transition: 0.3s; text-align: center; }
.card:hover { transform: translateY(-5px); box-shadow: 0 20px 40px rgba(15,23,42,0.08); }
.card h3 { font-size: 22px; margin-bottom: 15px; color: var(--primary); }
.card .icon { font-size: 40px; margin-bottom: 15px; display: block; }
.card p { color: var(--muted); font-size: 16px; }

/* Footer */
.footer { background: #0b1220; color: #cbd5e1; text-align: center; padding: 40px 0; margin-top: 50px; border-radius: 40px 40px 0 0; }
.footer h4 { color: white; font-size: 20px; margin-bottom: 10px; }
.footer p { color: var(--gold); }
"""

# ==========================================
# 🏗️ قالب اصلی (HTML)
# ==========================================
BASE_HTML = """
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>مدرسه آریو مصلی‌نژاد</title>
    <style>{{ css | safe }}</style>
</head>
<body>
    <nav class="navbar">
        <div class="container nav-inner">
            <a href="/" class="brand">
                <div class="logo">آ</div>
                <div>
                    <div style="font-weight:bold;">آریو مصلی‌نژاد</div>
                    <div style="font-size:12px; color:var(--muted);">ارومیه • نمونه دولتی</div>
                </div></a>
            <div class="nav-links">
                <a href="/">خانه</a>
                <a href="/about">درباره ما</a>
                <a href="/staff">کادر مدرسه</a>
                <a href="/activities">فعالیت‌ها</a>
                <a href="/contact">تماس</a>
            </div>
        </div>
    </nav>

    <main>
        {{ content | safe }}
    </main>

    <footer class="footer">
        <div class="container">
            <h4>دبیرستان نمونه دولتی آریو مصلی‌نژاد ارومیه</h4>
            <p>«درس، ایده، حال خوب»</p>
            <div style="margin-top:15px; font-size:13px;">© تمامی حقوق محفوظ است.</div>
        </div>
    </footer>
</body>
</html>
"""

# ==========================================
# 📄 محتوای صفحات
# ==========================================

HOME_CONTENT = """
<section class="hero">
    <div class="container">
        <h1>جایی که <span>درس، ایده و حال خوب</span><br>کنار هم می‌نشینند.</h1>
        <p>ما یک مدرسه نیستیم؛ یک تیمیم. تیمی از دانش‌آموزهای کنجکاو، دبیرهای پایه‌کار و کادری که بلدند از صبح تا ظهر، مدرسه را به جای بهتری برای بودن تبدیل کنند.</p>
        <a href="/about" class="btn">بیشتر بدانید</a>
    </div>
</section>
<section class="section container">
    <div class="grid">
        <div class="card">
            <span class="icon">🎯</span>
            <h3>درس با برنامه، نه با استرس</h3>
            <p>برنامه‌ریزی درست، کلاس‌های منظم و پشتیبانی معلم‌ها برای رسیدن به بهترین نتیجه.</p>
        </div>
        <div class="card">
            <span class="icon">🤝</span>
            <h3>احترام و کار تیمی</h3>
            <p>یاد می‌گیریم با هم بهتر یاد بگیریم، بهتر کار کنیم و بهتر زندگی کنیم.</p>
        </div>
        <div class="card">
            <span class="icon">🚀</span>
            <h3>فرصت دیده‌شدن</h3>
            <p>هر دانش‌آموز یک استعداد دارد؛ کار ما در آریو، کشف و پرورش آن است.</p>
        </div>
    </div>
</section>
"""

ABOUT_CONTENT = """
<section class="hero">
    <div class="container">
        <h1>درباره مدرسه</h1>
        <p>آریو مصلی‌نژاد فقط یک اسم روی سربرگ نیست.</p>
    </div>
</section>
<section class="section container">
    <div class="grid">
        <div class="card">
            <span class="icon">🏫</span>
            <h3>ما کی هستیم</h3>
            <p>یک مدرسه نمونه دولتی پسرانه در ارومیه که زیر نظر مدیریت جناب آقای سلاطین اداره می‌شود.</p>
        </div>
        <div class="card">
            <span class="icon">📚</span>
            <h3>روش ما</h3>
            <p>ترکیبی از آموزش منظم، فعالیت‌های دانش‌آموزی و فضای دوستانه؛ تا یاد گرفتن، لذت‌بخش هم باشد.</p>
        </div>
    </div>
</section>
"""

STAFF_CONTENT = """
<section class="hero">
    <div class="container">
        <h1>کادر مدیریت</h1>
        <p>آدم‌هایی که مدرسه را می‌چرخانند.</p>
    </div>
</section>
<section class="section container">
    <div class="grid">
        <div class="card">
            <span class="icon">👨‍💼</span>
            <h3>جناب آقای سلاطین</h3>
            <p style="color:var(--primary); font-weight:bold;">مدیر مدرسه</p>
        </div>
        <div class="card">
            <span class="icon">📝</span>
            <h3>جناب آقای الوائی</h3>
            <p style="color:var(--primary); font-weight:bold;">معاون آموزشی</p>
        </div>
        <div class="card">
            <span class="icon">🎭</span>
            <h3>معاون پرورشی</h3>
            <p>در حال تکمیل...</p>
        </div>
    </div>
</section>
"""

ACTIVITIES_CONTENT = """
<section class="hero">
    <div class="container">
        <h1>فعالیت‌های دانش‌آموزی</h1>
        <p>درس که تمام می‌شود، آریو تازه شروع می‌شود.</p>
    </div>
</section>
<section class="section container">
    <div class="grid">
        <div class="card">
            <span class="icon">🏅</span>
            <h3>المپیاد ورزشی</h3>
            <p>رقابت سالم بین کلاس‌ها در رشته‌های مختلف ورزشی.</p></div>
        <div class="card">
            <span class="icon">📰</span>
            <h3>نشریه دانش‌آموزی</h3>
            <p>قلم و ایده دانش‌آموزهای آریو، روی کاغذ.</p>
        </div>
        <div class="card">
            <span class="icon">🚌</span>
            <h3>اردوهای علمی و تفریحی</h3>
            <p>یادگیری بیرون از کلاس، همراه با خنده و خاطره.</p>
        </div>
    </div>
</section>
"""

CONTACT_CONTENT = """
<section class="hero">
    <div class="container">
        <h1>تماس با ما</h1>
        <p>حرفی داری؟ زنگ بزن یا سر بزن.</p>
    </div>
</section>
<section class="section container">
    <div class="grid">
        <div class="card">
            <span class="icon">📍</span>
            <h3>آدرس</h3>
            <p>ارومیه، محله بازار باش، میدان جانبازان، خیابان جانبازان</p>
        </div>
        <div class="card">
            <span class="icon">📞</span>
            <h3>تلفن</h3>
            <p>۰۴۴-۳۸۶۸۷۶۸۶</p>
        </div>
    </div>
</section>
"""

# ==========================================
# 🚦 مسیرهای سایت (Routes)
# ==========================================

@app.route("/")
def home():
    return render_template_string(BASE_HTML, content=HOME_CONTENT, css=CSS)

@app.route("/about")
def about():
    return render_template_string(BASE_HTML, content=ABOUT_CONTENT, css=CSS)

@app.route("/staff")
def staff():
    return render_template_string(BASE_HTML, content=STAFF_CONTENT, css=CSS)

@app.route("/activities")
def activities():
    return render_template_string(BASE_HTML, content=ACTIVITIES_CONTENT, css=CSS)

@app.route("/contact")
def contact():
    return render_template_string(BASE_HTML, content=CONTACT_CONTENT, css=CSS)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)