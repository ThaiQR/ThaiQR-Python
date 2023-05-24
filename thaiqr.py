from promptpay_type import PromptpayType
from transaction_uasge_type import TransactionUsageType
import crc16

def MerchantPromptpayQRGenerate( promptpayType: PromptpayType, receiveId: str, amount: str, transactionUsage: TransactionUsageType) -> str:

    if promptpayType is None:
        raise ValueError("Missing required parameter: promptpayType")
    
    if promptpayType == PromptpayType.MOBILE_NUMBER:
        receiveId = "0066" + receiveId[1:]
        receiveId = _preprocess_value(prefix="01", value=receiveId)
    elif promptpayType == PromptpayType.NATIONAL_ID:
        receiveId = _preprocess_value(prefix="02", value=receiveId)
    elif promptpayType == PromptpayType.E_WALLET_ID:
        receiveId = _preprocess_value(prefix="03", value=receiveId)
    elif promptpayType == PromptpayType.BANK_ACCOUNT:
        receiveId = _preprocess_value(prefix="03", value=receiveId)
    else:
        receiveId = ""
        
    pim_value: str
    if (transactionUsage == TransactionUsageType.ONETIME):
        pim_value = "12"
    elif (transactionUsage == TransactionUsageType.MANY_TIME):
        pim_value = "11"
    else:
        pim_value = ""
    
    PFI = _preprocess_value(prefix="00", value="01")
    PIM = _preprocess_value(prefix="01", value=pim_value)
    
    """Merchant Identifier"""
    AID = _preprocess_value(prefix="00", value="A000000677010111")
    merchanSum = AID + receiveId
    merchnatIdentifier = _preprocess_value(prefix="29", value=merchanSum)
    
    Currency = _preprocess_value(prefix="53", value="764")
    amount = _preprocess_amount(amount=amount)
    CountryCode = _preprocess_value(prefix="58", value="TH") 

    CRC = "6304"
        
    data = PFI + PIM + merchnatIdentifier + Currency + amount + CountryCode + CRC
    
    crc16Result = hex(crc16.crc16xmodem(data.encode('ascii'), 0xffff)).replace('0x', '')
    if len(crc16Result) < 4:  
        crc16Result = ("0"*(4-len(crc16Result))) + crc16Result
    data += crc16Result.upper()

    return data
    
    
def MerchantBillpaymentQRGenerate( billerId: str, merchantName: str, reference1: str, reference2: str, amount: str, transactionUsage: TransactionUsageType) -> str:
    
    pim_value: str
    if (transactionUsage == TransactionUsageType.ONETIME):
        pim_value = "12"
    elif (transactionUsage == TransactionUsageType.MANY_TIME):
        pim_value = "11"
    else:
        pim_value = ""

    PFI = _preprocess_value(prefix="00", value="01")
    PIM = _preprocess_value(prefix="01", value=pim_value)
    
    """Merchant Identifier"""
    AID = _preprocess_value(prefix="00", value="A000000677010112")
    billerId = _preprocess_value(prefix="01", value=billerId)
    reference1 = _preprocess_value(prefix="02", value=reference1)
    reference2 = _preprocess_value(prefix="03", value=reference2)
    merchantSum = AID + billerId + reference1 + reference2
    merchantIdentifier = _preprocess_value(prefix="30", value=merchantSum)
    
    Currency = _preprocess_value(prefix="53", value="764")
    amount = _preprocess_amount(amount=amount)
    CountryCode = _preprocess_value(prefix="58", value="TH") 
    
    merchantName = _preprocess_value(prefix="59", value=merchantName)
    
    CRC = "6304"
    
    data = PFI + PIM + merchantIdentifier + Currency + amount + CountryCode + merchantName + CRC
    
    crc16Result = hex(crc16.crc16xmodem(data.encode('ascii'), 0xffff)).replace('0x', '')
    if len(crc16Result) < 4:  
        crc16Result = ("0"*(4-len(crc16Result))) + crc16Result
    data += crc16Result.upper()

    return data
    
def _preprocess_value( prefix: str, value: str) -> str:
    if len(value) != 0:
        if len(value) < 10:
            value = prefix + "0" + str(len(value)) + value
        else:
            value = prefix + str(len(value)) + value
    else:
        value = ""
    
    return value

def _preprocess_amount( amount: str) -> str:
    check_amount = amount.split(".")

    if len(check_amount) > 1:
        if check_amount[1] == "" or len(check_amount[1]) == 0:
            check_amount[1] = "00"
        elif len(check_amount[1]) == 1:
            check_amount[1] += "0"
        elif len(check_amount[1]) > 2:
            check_amount[1] = check_amount[1][:2]

        amount = check_amount[0] + "." + check_amount[1]
    elif len(check_amount) == 1:
        amount = amount + "." + "00"

    amount = _preprocess_value("54", amount)

    return amount
    
