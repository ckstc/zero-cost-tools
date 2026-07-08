# -*- coding: utf-8 -*-
"""
promo_content.py — 种子流量用的「真实、有价值、非 spam」文案。

原则：
- 只发「对读者有用」的内容（工具/教程/资源），顺带带站点链接，不硬广。
- 每条都因地制宜（贴子标题、社区调性不同），避免同一段话到处复读被判定 spam。
- 链接统一指向站点根；具体工具可深链到 /store/ 或某个工具页。

这些文案由 automation/seed_traffic.py 自动发布；你只需在脚本暂停时登录对应账号。
"""

SITE_URL = "https://ckstc.github.io/zero-cost-tools/"

# ---------------------------------------------------------------------------
# Reddit（英文社区，重「分享创造 / 自托管 / 省钱 / 学编程」）
# 每个 subreddit 单独标题与正文，符合版规、先给价值再给链接。
# ---------------------------------------------------------------------------
REDDIT_POSTS = [
    {
        "subreddit": "selfhosted",
        "title": "I built a collection of 27 free, privacy-first, fully client-side web tools (no server, no tracking)",
        "body": (
            "Sharing something I put together: a set of 27 online tools that all run 100% in your "
            "browser — images, PDFs, text and JSON never leave the device. No signup, no analytics, "
            "no backend cost (hosted on GitHub Pages).\n\n"
            "Useful bits: image compressor, PDF tools, QR generator, base64/URL codec, timestamp "
            "converter, regex tester, CSV<->JSON, and more. Each has an SEO-friendly tutorial page too.\n\n"
            f"Live: {SITE_URL}\n\n"
            "Feedback / tool requests welcome — what would you add?"
        ),
    },
    {
        "subreddit": "learnprogramming",
        "title": "A free toolbox of browser-only utilities I wish I had when starting out",
        "body": (
            "When I was learning to code, I kept pasting data into random sites I didn't trust. "
            "So I made a set of 27 tiny tools that run entirely client-side (your text/files never "
            "upload anywhere): JSON formatter, regex tester, hash tool, UUID/batch generators, etc.\n\n"
            f"Open source + free: {SITE_URL}\n\n"
            "Hope it helps someone else skip the sketchy-site phase."
        ),
    },
    {
        "subreddit": "Frugal",
        "title": "Free, no-account-needed tools that quietly save money (privacy-friendly too)",
        "body": (
            "A small PSA: a lot of 'free' online tools make money by harvesting your data or hiding "
            "paywalls. I assembled 27 that are genuinely free, need no account, and run locally in "
            "the browser (compress images, convert files, generate codes, etc.).\n\n"
            f"Here: {SITE_URL}\n\n"
            "Pair it with library/FOSS alternatives and the savings add up."
        ),
    },
    {
        "subreddit": "webdev",
        "title": "27 free client-side utilities you can fork for your own projects (MIT)",
        "body": (
            "Built a bundle of 27 MIT-licensed, pure-frontend utilities — handy as building blocks or "
            "for quickly spinning up a privacy-respecting tool site. Everything is static, deployable "
            "to GitHub Pages in one push.\n\n"
            f"Repo/tools: {SITE_URL}\n\n"
            "Open to PRs and tool ideas."
        ),
    },
]

# ---------------------------------------------------------------------------
# V2EX（中文技术社区，节点：分享创造 / 程序员 / 免费资源 / 分享发现）
# ---------------------------------------------------------------------------
V2EX_POSTS = [
    {
        "node": "分享创造",
        "title": "做了个完全本地运行、零上传的免费在线工具箱（27 个，开源 MIT）",
        "content": (
            "纯前端实现，所有处理都在浏览器本地完成，图片/文本/文件**不会上传到任何服务器**，"
            "没有账号、没有埋点、没有后端成本（GitHub Pages 白嫖）。\n\n"
            "包含：图片压缩、PDF 工具、二维码、JSON 格式化、正则测试、哈希、UUID 批量生成、"
            "CSV/JSON 互转等 27 个。每个工具都配了 SEO 教程页。\n\n"
            f"在线地址：{SITE_URL}\n\n"
            "欢迎提需求或吐槽，下一步想加什么工具？"
        ),
    },
    {
        "node": "程序员",
        "title": "分享一组可白嫖部署的纯前端小工具（MIT，可直接 fork 改）",
        "content": (
            "写代码时老要把数据贴进不信任的站点，于是自己撸了一套 27 个纯前端工具，"
            "全部本地运行不上传。已开源，整套静态站一条命令就能部署到 GitHub Pages。\n\n"
            f"{SITE_URL}\n\n"
            "有想加的工具类型可以留言。"
        ),
    },
    {
        "node": "免费资源",
        "title": "27 个免费、免登录、本地运行的在线工具合集",
        "content": (
            "不想注册又想要顺手的小工具？这套全部免登录、本地运行、不上传数据："
            "压缩/转换/生成/编码解码都有。\n\n"
            f"{SITE_URL}"
        ),
    },
]

# ---------------------------------------------------------------------------
# 知乎（回答「有哪些好用的免费在线工具？」类问题）
# ---------------------------------------------------------------------------
ZHIHU_ANSWERS = [
    {
        "question": "有哪些好用的免费在线工具？",
        "answer": (
            "推荐一个我自己用的：一套「完全本地运行、零上传」的免费在线工具箱，27 个工具，"
            "全部在浏览器里处理，图片/文本/文件不会传到任何服务器，也不用注册。\n\n"
            "常用到的有：图片压缩、PDF 转图片、二维码生成、JSON 格式化、正则表达式测试、"
            "文本哈希、UUID 批量生成、CSV 与 JSON 互转、时间戳转换等。\n\n"
            f"地址：{SITE_URL}（开源 MIT，可自己部署一份）。\n\n"
            "适合在意隐私、又不想到处注册账号的人。"
        ),
    },
]

# ---------------------------------------------------------------------------
# 微博 / 朋友圈（短文案，口语化，带价值点）
# ---------------------------------------------------------------------------
WEIBO_POSTS = [
    f"攒了一套完全本地运行、不用注册、不上传数据的免费在线小工具（图片压缩/PDF/二维码/JSON/正则/哈希…共 27 个），开源 MIT，已部署。需要的自取 👉 {SITE_URL}",
]

WECHAT_MOMENTS = [
    f"分享个自用的免费工具箱：27 个纯前端小工具，本地运行不传数据、免登录，开源可自部署。图片压缩、PDF、二维码、JSON、正则、哈希都有 👉 {SITE_URL}",
]
