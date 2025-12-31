# import asyncio
# from app.utils.email import conf
# from fastapi_mail import FastMail, MessageSchema

# async def test():
#     message = MessageSchema(
#         subject="SES Test Email",
#         recipients=["vcare.kush.rahul@gmail.com"],
#         body="🎉 SES Email working!",
#         subtype="plain"
#     )

#     fm = FastMail(conf)
#     await fm.send_message(message)

# if __name__ == "__main__":
#     asyncio.run(test())
