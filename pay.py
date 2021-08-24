import requests, json

def first_register_do(userName, password, orderNumber, amount, clientId):
    resp = requests.post("https://3dsec.sberbank.ru/payment/rest/register.do", data = {
        "userName":userName,
        "password":password,
        "orderNumber":orderNumber,
        "amount":amount,
        "clientId":clientId,
        #"bindingId":"mva",
        #"features":"AUTO_PAYMENT",
        "returnUrl":"https://hr-tv.ru/successpayment",
        "failUrl":"https://hr-tv.ru/failpayment"
    })

    #print(resp.url)
    #print(resp.json())
    return resp.json()["orderId"] 

def register_do(bindingId):
    resp = requests.post("https://3dsec.sberbank.ru/payment/rest/register.do", data = {
        "userName":"T772370181045-api",
        "password":"T772370181045",
        "orderNumber":"-8",
        "amount":"100",
        "clientId":"mva",
        "bindingId":bindingId,
        "features":"AUTO_PAYMENT",
        "returnUrl":"https://hr-tv.ru/successpayment",
        "failUrl":"https://hr-tv.ru/failpayment"
    })

    print(resp.url)
    print(resp.json())
    return resp.json()["orderId"] 

def paymentOrderBinding_do(bindingId, mdOrder, ip):
    resp = requests.post("https://3dsec.sberbank.ru/payment/rest/paymentOrderBinding.do", data = {
        "userName":"T772370181045-api",
        "password":"T772370181045",
        "mdOrder":mdOrder,
        "bindingId":bindingId,
        "ip":ip
    })

    print(resp.json())

def getBindings_do():
    resp = requests.post("https://3dsec.sberbank.ru/payment/rest/getBindings.do", data = {
        "userName":"T772370181045-api",
        "password":"T772370181045",
        "clientId":"mva",
        "bindingType":"CR"
    })

    print(resp.json())

def getOrderStatusExtended_do(orderId):
    resp = requests.post("https://3dsec.sberbank.ru/payment/rest/getOrderStatusExtended.do", data = {
        "userName":"T772370181045-api",
        "password":"T772370181045",
        "orderId":orderId
    })

    #print(resp.json())
    #print(resp.json()["attributes"][0]["value"]) #mdOrder
    return (resp.json()["bindingInfo"]["bindingId"], resp.json()["ip"], resp.json()["attributes"][0]["value"])

def final_getOrderStatusExtended_do(orderId):
    resp = requests.post("https://3dsec.sberbank.ru/payment/rest/getOrderStatusExtended.do", data = {
        "userName":"T772370181045-api",
        "password":"T772370181045",
        "orderId":orderId
    })

    print(resp.json())

if __name__ == '__main__':
    #orderId = "78b69530-c1ef-776f-a5be-212827e3a83c"
    
    orderId = first_register_do() #первоначальный платеж. Тут получаем OrderId
    (bindingId, ip, mdOrder) = getOrderStatusExtended_do(orderId) #сведения о платеже. Тут получаем BindingId, только после оплаты клиентом
    orderId = register_do(bindingId) #платеж с настройками автоплатежа.
    
    #orderId = "3470701d-0025-7c62-a8c4-e1ab27e3a83c"
    
    paymentOrderBinding_do(bindingId, mdOrder, ip)
    final_getOrderStatusExtended_do(orderId)

#72a10429-17e3-70bb-8a70-356127e3a83c - OrderId
#bfc7b652-f628-7e62-a7e2-e5d727e3a83c - BindingId