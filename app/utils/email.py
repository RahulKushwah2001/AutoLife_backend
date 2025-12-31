# import os
# from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
# from dotenv import load_dotenv

# load_dotenv()

# conf = ConnectionConfig(
#     MAIL_USERNAME=os.getenv("AWS_SES_USERNAME"),
#     MAIL_PASSWORD=os.getenv("AWS_SES_PASSWORD"),
#     MAIL_FROM=os.getenv("MAIL_FROM"),
#     MAIL_PORT=587,
#     MAIL_SERVER="email-smtp.ap-southeast-2.amazonaws.com",  # SES SMTP endpoint
#     MAIL_STARTTLS=True,     # ✅ REQUIRED (NEW)
#     MAIL_SSL_TLS=False,     # ✅ REQUIRED (NEW)
#     USE_CREDENTIALS=True,
#     VALIDATE_CERTS=True,
# )

# async def send_email(subject: str, recipients: list[str], body: str):
#     message = MessageSchema(
#         subject=subject,
#         recipients=recipients,
#         body=body,
#         subtype="html"
#     )

#     fm = FastMail(conf)
#     await fm.send_message(message)
