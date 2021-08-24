import requests, json

UserName = "T772370181045-api"
Password = "T772370181045"

def first_register_do(orderNumber, amount, clientId):
    resp = requests.post("https://3dsec.sberbank.ru/payment/rest/register.do", data = {
        "userName":UserName,
        "password":Password,
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
        "userName":UserName,
        "password":Password,
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
        "userName":UserName,
        "password":Password,
        "mdOrder":mdOrder,
        "bindingId":bindingId,
        "ip":ip
    })

    return resp.json()

def getBindings_do():
    resp = requests.post("https://3dsec.sberbank.ru/payment/rest/getBindings.do", data = {
        "userName":UserName,
        "password":Password,
        "clientId":"mva",
        "bindingType":"CR"
    })

    print(resp.json())

def getOrderStatusExtended_do(orderId):
    resp = requests.post("https://3dsec.sberbank.ru/payment/rest/getOrderStatusExtended.do", data = {
        "userName":UserName,
        "password":Password,
        "orderId":orderId
    })

    #print(resp.json())
    #print(resp.json()["attributes"][0]["value"]) #mdOrder
    return (resp.json()["bindingInfo"]["bindingId"], resp.json()["ip"], resp.json()["attributes"][0]["value"])

def final_getOrderStatusExtended_do(orderId):
    resp = requests.post("https://3dsec.sberbank.ru/payment/rest/getOrderStatusExtended.do", data = {
        "userName":UserName,
        "password":Password,
        "orderId":orderId
    })

    return resp.json()

if __name__ == '__main__':
    
    orderId = first_register_do() #первоначальный платеж. Тут получаем OrderId
    (bindingId, ip, mdOrder) = getOrderStatusExtended_do(orderId) #сведения о платеже. Тут получаем BindingId, только после оплаты клиентом
    orderId = register_do(bindingId) #платеж с настройками автоплатежа.
    
    
    paymentOrderBinding_do(bindingId, mdOrder, ip)
    final_getOrderStatusExtended_do(orderId)