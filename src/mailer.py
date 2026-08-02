import smtplib
from email.mime.text import MIMEText
from typing import List


def send_email(
    smtp_host: str,
    smtp_port: int,
    username: str,
    password: str,
    from_addr: str,
    to_addrs: List[str],
    subject: str,
    body: str,
) -> None:
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_addr
    msg["To"] = ", ".join(to_addrs)

    with smtplib.SMTP(smtp_host, smtp_port, timeout=30) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(from_addr, to_addrs, msg.as_string())
