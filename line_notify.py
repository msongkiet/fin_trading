import requests

def line_notify(msg, token):
    url_line_noti = 'https://notify-api.line.me/api/notify'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}
    r = requests.post(url_line_noti, headers=headers, data = {'message': msg})
    print(r.text)