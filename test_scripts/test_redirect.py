import sys
sys.path.append('../')

from features import check_redirection as ck_rd



l = ["https://tinyurl.com/mpdbcbu9", "https://youtu.be/Bm7L-2J52GU", "https://ddg.gg",
    "https://free-url-shortener.rb.gy/",
    "http://www.google.com","https://www.google.com", "https://tinyurl.com/bp5855zt"]# "http://bitly.ws/A7Hx"]


for i in l:
    print(f"[+] {i} :\n  ret:{ck_rd.check_redirect(i)}\n",end='')