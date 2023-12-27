import ssl
import subprocess
import time
from smtplib import SMTP_SSL

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

TEMP_THRESHOLD = 70

def get_cpu_temperature():
    # シェルコマンドを実行
    result = subprocess.run(["sensors | grep 'Package id 0' | awk '{print $4}' | cut -c 2-3"], stdout=subprocess.PIPE, shell=True)
    # 結果を文字列として取得、整数値に変換
    temp = int(result.stdout.strip())
    return temp

def create_mail_message_mime(from_email, to_email, message, subject, filepath=None, filename=""):
    # MIMETextを作成
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.attach(MIMEText(message, 'plain', 'utf-8'))
    return msg

def send_email(msg):
    account = "             @gmail.com"  # Your Gmail address
    password = "                  "   # Your Gmail password

    host = 'smtp.gmail.com'
    port = 465

    context = ssl.create_default_context()
    server = SMTP_SSL(host, port, context=context)

    server.login(account, password)

    server.send_message(msg)

    server.quit()

def main():
    temp = get_cpu_temperature()
    if temp >= TEMP_THRESHOLD:
        # メールの送り主
        from_email = "                          " 

        # メール送信先
        to_email = "                             " 

        subject = "[警告!]サーバーの温度異常"
        message = f"自宅サーバーのCPU温度が{temp}度です."

        # MIME形式の作成
        mime = create_mail_message_mime(from_email, to_email, message, subject)

        # メールの送信
        send_email(mime)
    
if __name__ == "__main__":
    main()