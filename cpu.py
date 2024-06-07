import os
import ssl
import subprocess
import time
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

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
    account = os.getenv('EMAIL_ACCOUNT')
    password = os.getenv('EMAIL_PASSWORD')

    host = 'smtp.gmail.com'
    port = 465

    context = ssl.create_default_context()
    server = SMTP_SSL(host, port, context=context)

    server.login(account, password)

    server.send_message(msg)

    server.quit()

def main():
    load_dotenv()
    temp = get_cpu_temperature()
    if temp >= TEMP_THRESHOLD:
        from_email = os.getenv('EMAIL_ACCOUNT')
        to_emails = os.getenv('TO_EMAILS').split(',')
        subject = "[警告!]サーバーの温度異常"
        message = f"自宅サーバーのCPU温度が{temp}度です."
        for to_email in to_emails:
            # MIME形式の作成
            mime = create_mail_message_mime(from_email, to_email, message, subject)     
            # メールの送信
            send_email(mime)
    
if __name__ == "__main__":
    main()