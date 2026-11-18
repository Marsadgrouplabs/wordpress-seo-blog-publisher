<p align="center"><a href="README.md">English</a> · <b>العربية</b></p>

<p align="center"><img src=".github/assets/banner.ar.svg" width="100%" alt="WordPress SEO Blog Publisher: من اسم الموضوع لمقال منشور على موقعك"></p>

> **من اسم الموضوع لمقال منشور على موقعك.** تاخد اسم موضوع وتعمل بحث، وتكتب المقال عن طريق `seo-blog-write-ar-en`، وتجهّز الصور والتصنيفات، وتنشر على WordPress عن طريق REST API. قيم RankMath والـ Schema بتتسلم لك جاهزة للصق.

## بتشتغل إزاي؟

<p align="center"><img src=".github/assets/flow.ar.svg" width="100%" alt="الخطوات: اكتب الموضوع، بحث وكتابة، تجهيز المقال، النشر"></p>

## قولها كده وسيبها تشتغل

- «انشر بلوج عن الموضوع ده على موقعي»
- «اكتب مقال وانزله على الموقع»

## النتايج (بهزر، بس بجد مفيدة)

<p align="center"><img src=".github/assets/chart.ar.svg" width="100%" alt="رسم فكاهي غير علمي. تابات مفتوحة للبحث: 96% من غيرها و15% معاها؛ نسخ ولصق في WordPress: 90% من غيرها و5% معاها؛ وقت الشاي: 10% من غيرها و88% معاها"></p>

## ركّبها في دقيقة

| بتستخدم إيه؟ | الطريقة |
|---|---|
| حساب Claude أو ChatGPT | نزّل [`wordpress-seo-blog-publisher.zip`](https://github.com/Marsadgrouplabs/wordpress-seo-blog-publisher/releases/latest/download/wordpress-seo-blog-publisher.zip) وارفعه من قسم Skills |
| Claude Code | `claude plugin marketplace add Marsadgrouplabs/wordpress-seo-blog-publisher` |
| Claude Code أو Codex بسكربت | حمّل الـ repo وشغّل `install.ps1` أو `install.sh` |

<details>
<summary><b>الخطوات بالتفصيل</b></summary>

### حساب Claude أو ChatGPT

1. نزّل [`wordpress-seo-blog-publisher.zip`](https://github.com/Marsadgrouplabs/wordpress-seo-blog-publisher/releases/latest/download/wordpress-seo-blog-publisher.zip) وماتفكّهوش.
2. **Claude:** افتح قسم Skills في حسابك واختار رفع ملف.
3. **ChatGPT:** افتح Skills، ثم Create، ثم Upload from your computer. الميزة متاحة حسب خطة الحساب.

### Claude Code كـ Plugin

```bash
claude plugin marketplace add Marsadgrouplabs/wordpress-seo-blog-publisher
claude plugin install wordpress-seo-blog-publisher@marsad-wordpress-seo-blog-publisher
```

### ويندوز

```powershell
git clone https://github.com/Marsadgrouplabs/wordpress-seo-blog-publisher.git
cd wordpress-seo-blog-publisher
powershell -ExecutionPolicy Bypass -File .\install.ps1
```

### ماك أو لينكس

```bash
git clone https://github.com/Marsadgrouplabs/wordpress-seo-blog-publisher.git
cd wordpress-seo-blog-publisher
bash install.sh
```

السكربت بيركّبها لـ Claude Code في `~/.claude/skills` ولـ Codex في `~/.agents/skills`، ولو فيه نسخة قديمة بيحتفظ بيها.

</details>

## مطمنك: مين الناشر وبياناتك فين؟

الناشر هو **[Marsad Labs](https://labs.marsadgroup.co)**. Marsad Labs هي ذراع المنتجات في Marsad Group، شركة تسويق مسجلة في بريطانيا، وبتبني أدوات عملية للمسوقين والمطورين. [اعرف أكتر عننا](https://labs.marsadgroup.co/about-us/) · [سياسة الخصوصية](https://labs.marsadgroup.co/privacy-policy/)

| السؤال | الإجابة |
|---|---|
| **بيانات الدخول** | بتفضل في ملف `sites.txt` على جهازك، ومابتترفعش مع الـ skill ولا بتتطبع. |
| **بتتصل بإيه؟** | سكربت `wp.py` بيتصل بمواقع WordPress اللي انت كتبتها في الملف بس. |
| **بتنشر لوحدها؟** | أيوه لما تطلب منها نشر مقال: بتعمل Draft الأول وبعدين تنشره. استخدم Application Password بصلاحية مناسبة. |
| **الكود** | سكربت واحد مكتوب بمكتبات Python الأساسية ومفتوح تقراه بنفسك. |

النسخة دي اتفحصت بأداة SkillSpector، واتراجعت تنبيهاتها الحرجة والعالية يدوياً، واتشال منها أي بيانات عملاء أو مفاتيح. النتيجة الكاملة وطريقة التأكد من الملف والإبلاغ عن مشكلة في [`SECURITY.ar.md`](SECURITY.ar.md).

## محتاج إيه؟

- Python 3.
- موقع WordPress عليه RankMath، وApplication Password لمستخدم له صلاحية النشر.
- تركيب skill اسمها `seo-blog-write-ar-en` معاها.

## قبل ما تبدأ

- **إعداد المواقع مرة واحدة:** انسخ `scripts/sites.example.txt` إلى `~/.wp-publisher/sites.txt` واكتب فيه بيانات موقعك. الملف ده بيفضل على جهازك ومابيترفعش أبداً.
- **النشر الفعلي** محتاج Claude Code أو Codex على الجهاز، لأن بيانات الدخول موجودة هناك.

## الحقوق

كل الحقوق محفوظة لـ Marsad Labs. ممنوع النسخ أو إعادة النشر بدون إذن.

---

<p align="center">معمولة بحب وشاي كتير في <a href="https://labs.marsadgroup.co"><b>Marsad Labs</b></a></p>
