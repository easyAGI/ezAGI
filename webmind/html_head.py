# html_head.py

def add_head_html(ui):
    ui.add_head_html('<link rel="stylesheet" href="/gfx/easystyle.css">')
    ui.add_head_html('<title>EasyAGI Augmented Generative Intelligence</title>')
    ui.add_head_html('''<meta name="description" content="easyAGI augmented generative intelligence for LLM">''')
    ui.add_head_html('''<meta name="keywords" content="EasyAGI Augmented Generative Intelligence">''')
    ui.add_head_html('''<meta name="author" content="Gregory L. Magnusson">''')
    ui.add_head_html('''<meta name="license" content="MIT">''')
    ui.add_head_html('<link rel="icon" type="image/x-icon" href="/gfx/fav/favicon.ico">')
    ui.add_head_html('''<meta name="viewport" content="width=device-width, initial-scale=1.0">''')
    ui.add_head_html('<link rel="apple-touch-icon" sizes="180x180" href="/gfx/fav/apple-touch-icon.png">')
    ui.add_head_html('<link rel="icon" type="image/png" sizes="32x32" href="/gfx/fav/favicon-32x32.png">')
    ui.add_head_html('<link rel="icon" type="image/png" sizes="16x16" href="/gfx/fav/favicon-16x16.png">')
    ui.add_head_html('<link rel="manifest" href="/site.webmanifest">')

