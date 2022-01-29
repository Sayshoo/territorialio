import math

types = {
    int : lambda data : int.from_bytes(data, "big"),
    bytes : lambda data : bytes(data)
}
class Element:
    def __init__(self, size):
        self.size = size
        self.value = []

    def serialize(data, offset):
        result = []
        offset = 0
        for key in type:
            value = object[key]
            currentFieldSize = type[key][0] if type[key][0] > 0 else len(value)
            setBitData(result, offset, currentFieldSize, value)
            offset += currentFieldSize
        return result

lobbyConnect = {
    "id" : [ 4 , int ],
    "r" : [ 6, int ],
    "g" : [ 6, int ],
    "b" : [ 6, int ],
    "clutter" : [ 14 + 4 + 1 + 1 , int],
    "timeStampBytes" : [ 5, int ],
    "name" : [ -1, bytes]
}

seaAttack = {
    "id" : [ 4 , int ],
    "flag?" : [ 10 , int],
    "X" : [ 11, int ],
    "Y" : [ 11, int ]
}

landAttack = {
    "id" : [ 4 , int ],
    "count" : [ 10 , int],
    "player_id" : [ 9, int ]
}

def deserialize(data, type):
    resultObj = {}
    resultObj["_schema_"] = {}
    offset = 0
    totalDataLength = len(data)*8
    for key in type:
        currentFieldSize = type[key][0] if type[key][0] > 0 else totalDataLength - offset
        currentFieldType = type[key][1]
        
        currentFieldData = getBitData(data, offset, currentFieldSize)
        resultObj[key] = types[currentFieldType](currentFieldData)
        resultObj["_schema_"][key] = [currentFieldSize, currentFieldType]
        offset += currentFieldSize
    return resultObj

def serialize(object, type):
    result = []
    offset = 0
    for key in type:
        value = object[key]
        currentFieldSize = type[key][0] if type[key][0] > 0 else len(value) * 8
        setBitData(result, offset, currentFieldSize, value)
        offset += currentFieldSize
    return result

def setBitData(data, start, size, value):
    newBitsCount = size - start
    oldBytesCount = getRequiredBytes(start)
    newBytesCount = getRequiredBytes(start + size)
    deltaBytesCount = newBytesCount - oldBytesCount
    
    valueBytesCount = getRequiredBytes(size)
    totalSize = valueBytesCount * 8

    value = value if type(value) == bytes else value.to_bytes(valueBytesCount, "big") 
    #print(value.hex()) 

    #print("start %s size %s" %(start, size))

    # create new byte elements to list to accomodate new data
    data += [ 0x00 ] * deltaBytesCount
    #print(data)

    #print("di vi >> << bit")
    valueStart = totalSize - size
    for i in range(valueStart, totalSize): # i => index of value bits
        currentDataByteIndex = getByteOffset(start + i - valueStart)
        currentValueByteIndex = getByteOffset(i)

        #shiftRightAmount = 7 - i % 8 if size > 8 else 7 - size - i % 8
        #shiftRightAmount = 7 - size -  i % 8 
        shiftRightAmount = 7 - i % 8
        shiftLeftAmount = 7 - (start + i - valueStart) % 8

        extractedBit = value[currentValueByteIndex] >> shiftRightAmount & 1

        #      di vi >> << bit
        #print("%s  %s  %s  %s  %s" %(currentDataByteIndex, currentValueByteIndex, shiftRightAmount, shiftLeftAmount, extractedBit))

        data[currentDataByteIndex] |= extractedBit << shiftLeftAmount

def getBitData(data, startIndex, size):
    resultSize = math.ceil(size / 8) * 8
    resultBitIndex = resultSize - size

    result = [0x00] * math.ceil(size / 8)
    for i in range(startIndex, startIndex+size):
        currentDataByteIndex = getByteOffset(i)
        currentResultByteIndex = getByteOffset(resultBitIndex)

        shiftRightAmount = 7 - i % 8
        shiftLeftAmount = (resultSize - 1 - resultBitIndex) % 8

        currentDataByte = data[currentDataByteIndex]

        extractedBit = currentDataByte >> shiftRightAmount & 1

        result[currentResultByteIndex] |= extractedBit << shiftLeftAmount
        resultBitIndex += 1

    return result

def getByteOffset(bitOffset):
    return math.floor(bitOffset / 8)

def getRequiredBytes(bitsCount):
    return math.ceil(bitsCount / 8)

def getOrPush(arr, index):
    arr.append(1)

if __name__ == '__main__':

    
    
    #exit()
    
    data =  bytearray.fromhex('52edc206617670aa5add7bc02e79ab031e274ecb38e05e258802c088288000982a0800')

    obj = deserialize(data, lobbyConnect)
    print(obj)

    newData = serialize(obj, obj["_schema_"])

    print(bytes(newData).hex())

    exit()

    arr = [  ]

    setBitData(arr, 0, 4, 5)

    print(bytes(arr).hex())

    setBitData(arr, 4, 20, 5)

    print(bytes(arr).hex())

    exit()
    

