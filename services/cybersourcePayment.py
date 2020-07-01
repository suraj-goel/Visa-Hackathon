from CyberSource import *
import os
import json
from importlib.machinery import SourceFileLoader

config_file = os.path.join(os.getcwd(), "services/data", "Configuration.py")
configuration = SourceFileLoader("module.name", config_file).load_module()


def del_none(d):
    """
    :param d: Request Json body
    :return: deletes None values in Input Request Json body
    """
    for key, value in list(d.items()):
        if value is None:
            del d[key]
        elif isinstance(value, dict):
            del_none(value)
    return d


def simple_authorizationinternet(cardNumber="4111111111111111", cardExpirationMonth="12", cardExpirationYear="2031",
                                 amount="0", aggregator_id="123456789", card_acceptor_id="1234567890",
                                 name="V-Internatio"):
    """
    :param cardNumber: PAN assosiated with user
    :param cardExpirationMonth, cardExpirationYear: Card expiration date
    :param amount: amount to deduct from account
    :param aggregator_id: aggregator id registered with CyberSource
    :param card_acceptor_id: card accepter id registered with CyberSource
    :param name: registered name with CyberSource
    payment authorization and completeion
    """
    amount = str(float(amount) / 76.0)  # INR to USD for Visa API compatibility
    print(
        "\nCardNumber:" + cardNumber + "\nCardExpirationMonth:" + cardExpirationMonth + "\nCardExpirationYear:" + cardExpirationYear + "\nAmount:" + amount + "\nAGGID:" + aggregator_id + "\nCAID:" + card_acceptor_id + "\nName:" + name + "\n")
    flag = False
    clientReferenceInformationCode = "TC50711_3"
    clientReferenceInformation = Ptsv2paymentsClientReferenceInformation(
        code=clientReferenceInformationCode
    )

    processingInformationCapture = False
    if flag:
        processingInformationCapture = True

    processingInformation = Ptsv2paymentsProcessingInformation(
        capture=processingInformationCapture
    )

    paymentInformationCardNumber = cardNumber
    paymentInformationCardExpirationMonth = cardExpirationMonth
    paymentInformationCardExpirationYear = cardExpirationYear
    paymentInformationCard = Ptsv2paymentsPaymentInformationCard(
        number=paymentInformationCardNumber,
        expiration_month=paymentInformationCardExpirationMonth,
        expiration_year=paymentInformationCardExpirationYear
    )

    paymentInformation = Ptsv2paymentsPaymentInformation(
        card=paymentInformationCard.__dict__
    )

    orderInformationAmountDetailsTotalAmount = amount
    orderInformationAmountDetailsCurrency = "USD"
    orderInformationAmountDetails = Ptsv2paymentsOrderInformationAmountDetails(
        total_amount=orderInformationAmountDetailsTotalAmount,
        currency=orderInformationAmountDetailsCurrency
    )

    orderInformationBillToFirstName = "John"
    orderInformationBillToLastName = "Doe"
    orderInformationBillToAddress1 = "abc"
    orderInformationBillToLocality = "san francisco"
    orderInformationBillToAdministrativeArea = "CA"
    orderInformationBillToPostalCode = "94105"
    orderInformationBillToCountry = "IN"
    orderInformationBillToEmail = "test@cybs.com"
    orderInformationBillToPhoneNumber = "4158880000"
    orderInformationBillTo = Ptsv2paymentsOrderInformationBillTo(
        first_name=orderInformationBillToFirstName,
        last_name=orderInformationBillToLastName,
        address1=orderInformationBillToAddress1,
        locality=orderInformationBillToLocality,
        administrative_area=orderInformationBillToAdministrativeArea,
        postal_code=orderInformationBillToPostalCode,
        country=orderInformationBillToCountry,
        email=orderInformationBillToEmail,
        phone_number=orderInformationBillToPhoneNumber
    )

    orderInformation = Ptsv2paymentsOrderInformation(
        amount_details=orderInformationAmountDetails.__dict__,
        bill_to=orderInformationBillTo.__dict__
    )

    sub_merchant = Ptsv2paymentsAggregatorInformationSubMerchant(card_acceptor_id=card_acceptor_id, id=None, name=name,
                                                                 address1=None, locality=None, administrative_area=None,
                                                                 region=None, postal_code=None, country=None,
                                                                 email=None, phone_number=None)

    aggregatorInfo = Ptsv2paymentsAggregatorInformation(aggregator_id, name, sub_merchant=sub_merchant)

    requestObj = CreatePaymentRequest(
        client_reference_information=clientReferenceInformation.__dict__,
        processing_information=processingInformation.__dict__,
        payment_information=paymentInformation.__dict__,
        order_information=orderInformation.__dict__
    )

    requestObj = del_none(requestObj.__dict__)
    requestObj = json.dumps(requestObj)

    try:
        config_obj = configuration.Configuration()
        client_config = config_obj.get_configuration()
        api_instance = PaymentsApi(client_config)
        return_data, status, body = api_instance.create_payment(requestObj)

        print("\nAPI RESPONSE CODE : ", status)
        print("\nAPI RESPONSE BODY : ", body)
        print("\nAPI RETURN DATA : ", return_data)
        bodydict = eval(body)
        actualStatus = bodydict["status"]
        print("STATUS:", bodydict["status"])
        if (actualStatus == "DECLINED"):
            raise Exception
        else:
            return 1
    except Exception as e:
        print("\nException when calling PaymentsApi->create_payment: %s\n" % e)
        return 0

# if __name__ == "__main__":
#    simple_authorizationinternet()
