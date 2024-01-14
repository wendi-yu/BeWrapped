import requests

class BerealAPI:
    def __init__(self):
        self.api_url = "https://berealapi.fly.dev"
        self.endpoints = {
            "send_otp": "/login/send-code",
            "verify": "/login/verify",
            "memfeed": "/friends/mem-feed"
        }


    def send_otp(self, phone_number):
        url = self.api_url + self.endpoints["send_otp"]
        data = {"phone": phone_number}
        r = requests.post(url, data)
        # TODO: blah blah error handling

        # status code 201
        print(r.json())
        return r.json()["data"]["otpSession"]
    
    def verify_otp(self, otp, session):
        url = self.api_url + self.endpoints["verify"]
        data = {"code": otp, "otpSession": session}
        r = requests.post(url, data)

        return r.json()["data"]["token"]
    
    def login(self, phone_number):
        session = self.send_otp(phone_number)
        code = input("OTP code:")
        return self.verify_otp(code, session)
    

    def get_memfeed(self, token):
        url = self.api_url + self.endpoints["memfeed"]
        headers = {"token": token}
        r = requests.get(url, headers=headers)

        return r.json()["data"]["data"]
        


