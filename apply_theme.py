import os

def update_file(filename, task):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    content = task(content)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)

# 1. Update style.css
css_vars = """
:root {
  --c-n-50: 250 250 250;
  --c-n-100: 245 245 245;
  --c-n-200: 229 229 229;
  --c-n-300: 212 212 212;
  --c-n-400: 163 163 163;
  --c-n-500: 115 115 115;
  --c-n-600: 82 82 82;
  --c-n-700: 64 64 64;
  --c-n-800: 38 38 38;
  --c-n-900: 23 23 23;
  --c-n-950: 10 10 10;
  --c-white: 255 255 255;
  --c-amber-300: 252 211 77;
  --c-amber-400: 251 191 36;
  --c-amber-500: 245 158 11;
  --c-amber-600: 217 119 6;
  --c-amber-800: 146 64 14;
  --c-amber-900: 120 53 15;
  --c-red-300: 252 165 165;
  --c-red-400: 248 113 113;
  --c-red-500: 239 68 68;
  --c-red-600: 220 38 38;
  --c-red-900: 127 29 29;
  --c-green-400: 74 222 128;
  --c-green-500: 34 197 94;
  --c-green-600: 22 163 74;
  --c-green-900: 20 83 45;
  --c-sky-400: 56 189 248;
  --c-sky-900: 12 74 110;
  --c-violet-400: 167 139 250;
  --c-violet-900: 76 29 149;
}
.light-theme {
  --c-n-50: 10 10 10;
  --c-n-100: 23 23 23;
  --c-n-200: 38 38 38;
  --c-n-300: 64 64 64;
  --c-n-400: 82 82 82;
  --c-n-500: 115 115 115;
  --c-n-600: 163 163 163;
  --c-n-700: 212 212 212;
  --c-n-800: 229 229 229;
  --c-n-900: 245 245 245;
  --c-n-950: 250 250 250;
  --c-white: 10 10 10;
  --c-amber-300: 217 119 6;
  --c-amber-400: 180 83 9;
  --c-amber-500: 146 64 14;
  --c-amber-600: 120 53 15;
  --c-amber-800: 253 230 138;
  --c-amber-900: 254 243 199;
  --c-red-300: 220 38 38;
  --c-red-400: 185 28 28;
  --c-red-500: 153 27 27;
  --c-red-600: 127 29 29;
  --c-red-900: 254 226 226;
  --c-green-400: 21 128 61;
  --c-green-500: 22 101 52;
  --c-green-600: 20 83 45;
  --c-green-900: 187 247 208;
  --c-sky-400: 3 105 161;
  --c-sky-900: 224 242 254;
  --c-violet-400: 109 40 217;
  --c-violet-900: 237 233 254;
}
.light-theme img.invert {
  filter: none !important;
}
"""
def task_css(c):
    c = c.replace('\nbody {', '\n' + css_vars + '\nbody {')
    c = c.replace('#404040', 'rgb(var(--c-n-700))')
    c = c.replace('#171717', 'rgb(var(--c-n-900))')
    return c
update_file('style.css', task_css)

print("Updates applied.")
