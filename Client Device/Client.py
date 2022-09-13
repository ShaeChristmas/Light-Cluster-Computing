# Python Web Client
import http.client, json, random, time, sys
from unittest import result

start_ip = "192.168.1.100"
ips = []
ready = []
matrixTest = [1]
matrixC = [1,2,3,4,5,6,7,8,9]
matrixCP = [[1,2,3],[4,5,6],[7,8,9]]
matrixID = [1,0,0,0,1,0,0,0,1]
matrixIDP = [[1,0,0],[0,1,0],[0,0,1]]
matrixD = [2,4,6,8,10,12,14,16,18]
matrixDP = [[2,4,6],[8,10,12],[14,16,18]]
matrixResult = []

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept",
    "Content-Type": "application/json"
}

def convMat(matrix):
    matrixResult = []
    size = len(matrix)
    for i in range(size):
        for j in range(size):
            #print("i: "+str(i)+" j: "+str(j))
            matrixResult.append(matrix[i][j])
    print("Matrix Converted")
    return matrixResult

def createMatrix(size, val):
    matrix = []
    if val == 0:
        for i in range(size):
            matrix.append([])
            for j in range(size):
                matrix[i].append(val)
    else:
        for i in range(size):
            matrix.append([])
            for j in range(size):
                matrix[i].append(random.randint(1,10))
    return matrix

def multiplyLocal(matrix1, matrix2, matrixResult):
    m1Size = len(matrix1)
    for i in range(m1Size):
        for j in range(m1Size):
            for k in range(m1Size):
                #print("I: "+str(i)+" J: "+str(j)+" K: "+str(k))
                matrixResult[i][j] += matrix1[i][k] * matrix2[k][j]
    return matrixResult

def popIps(ip, print=True):
    # Copilot Example of using http.client
    # Create a connection to the server
    connection = http.client.HTTPConnection(ip, 5000)
    # Send a request to the server
    connection.request('GET', '/infoReq')
    # Read the response from the server
    response = connection.getresponse()
    # Decode the response
    data = response.read().decode()
    data = json.loads(data)
    for val in data:
        valueToAdd = json.loads(val)["ip"]
        ips.append(valueToAdd)
        if (print): 
            print(valueToAdd)
    connection.close()

def readyCheck():
    # Create a connection to the server
    connection = http.client.HTTPConnection(start_ip, 5000)
    # Send a request to the server
    connection.request('GET', '/compVal')
    # Read the response from the server
    response = connection.getresponse()
    # Decode the response
    data = response.read().decode()
    data = json.loads(data)
    # print(data)
    for val in data:
        valueToAdd = json.loads(val)
        # print(valueToAdd)
        if valueToAdd[1] == True:
            ready.append(valueToAdd[0])
    connection.close()

# NOTE: MATRICIES MUST BE SQUARE!!!
def multiply(matrix1, matrix2, ip=start_ip,number=0):
    body = {
        "matrixA": matrix1, 
        "matrixB":matrix2,
        "number":number
    }
    JSONbody = json.dumps(body).encode()
    #print(sys.getsizeof(JSONbody))
    #print(JSONbody)
    # Create a connection to the server
    connection = http.client.HTTPConnection(ip, 5000, timeout=5000)
    # Send a request to the server
    connection.request('GET', '/getComp',body=JSONbody,headers=headers)
    # Read the response from the server
    response = connection.getresponse()
    # Decode the response
    data = response.read().decode()
    data = json.loads(data)
    #print(data)
    return data

def CalcPi(Accuracy, ip=start_ip,number=0):
    body = {
        "accuracy": Accuracy,
        "number":number
    }
    JSONbody = json.dumps(body).encode()
    #print(sys.getsizeof(JSONbody))
    #print(JSONbody)
    # Create a connection to the server
    connection = http.client.HTTPConnection(ip, 5000, timeout=5000)
    # Send a request to the server
    connection.request('GET', '/getComp',body=JSONbody,headers=headers)
    # Read the response from the server
    response = connection.getresponse()
    # Decode the response
    data = response.read().decode()
    data = json.loads(data)
    #print(data)
    return data

def testWork():
    matrixResult = []
    # Print ips before
    print("Before: "+str(ips))
    # Populate ips
    popIps(start_ip)
    # Print ips after
    print("After: "+str(ips))
    # Print ready before
    print("Before: "+str(ready))
    # Check ready devices
    readyCheck()
    # Print ready after
    print("After: "+str(ready))
    # Print result matrix before calculation
    print("Result Matrix: "+str(matrixResult))
    # Multiply MatrixA and MatrixID
    print("Mutliplying: ", matrixC, "\n and ", matrixID)
    matrixResult = multiply(matrixC, matrixID)
    # Print result matrix after calculation
    print("Result Matrix: "+str(matrixResult))
    # Reset Result Matrix
    matrixResult = []
    # Print result matrix before calculation
    print("Result Matrix: "+str(matrixResult))
    # Multiply MatrixA and MatrixID
    print("Mutliplying: ", matrixC, "\n and ", matrixD)
    matrixResult = multiply(matrixC, matrixD)
    # Print result matrix after calculation
    print("Result Matrix: "+str(matrixResult))

def localTime(matrix1, matrix2):
    localResult = createMatrix(len(matrix1),0)
    #start timer.
    start = time.time()
    # multiply
    multiplyLocal(matrix1, matrix2, localResult)
    #stop timer.
    stop = time.time()
    print("Local Duration: ", stop-start)
    return [localResult, stop-start]

def offTime(matrix1, matrix2, number=0):
    offResult = createMatrix(len(matrix1),0)
    matrix1Temp = convMat(matrix2)
    matrix2Temp = convMat(matrix1)
    #start timer.
    start = time.time()
    # multiply
    offResult = multiply(matrix1Temp, matrix2Temp, start_ip, number)
    #stop timer.
    stop = time.time()
    print("Off Duration: ", stop-start)
    return [offResult,stop-start]

def runTest1(size): # Tests the flexibility in the size of the computation
    print("Size: "+str(size))
    QoS = False
    # Create matrix1
    matrixA = createMatrix(size,1)
    #print("MatrixA: "+str(matrixA))
    # Create matrix2
    matrixB = createMatrix(size,1)
    #print("MatrixB: "+str(matrixB))
    # Measure Time to multiply locally
    resultMatrixLocal = localTime(matrixA, matrixB)
    # Perform offloading with 1 device (Remember to start localhost API first)
    resultMatrixOff1 = offTime(matrixA, matrixB, number = 1)
    # Perform offloading with proposed Architecture
    resultMatrixOff3 = offTime(matrixA, matrixB, number = 3)
    #print(matrixA)
    #print(matrixB)
    #print(resultMatrixLocal)
    #print(resultMatrixOff)
    if(resultMatrixLocal[0] == resultMatrixOff3[0] and resultMatrixLocal[0] == resultMatrixOff1[0]):
        QoS = True
        #print("All results are the same")
    file =open("results/results1.txt", "a")
    file.write(str(size)+","+str(resultMatrixLocal[1])+","+str(resultMatrixOff1[1])+","+str(resultMatrixOff3[1])+","+str(QoS)+"\n")
    file.close()

def runTest2(devices): # Tests the flexibility in the number of devices used.
    print("Number of Devices: "+str(devices))
    QoS = True
    # Create matrix1 and matrix2
    matrixA = createMatrix(80,1)
    matrixB = createMatrix(80,1)

    matrixA = convMat(matrixA)
    matrixB = convMat(matrixB)

    resultVal = []
    for i in range(1,devices+1):
        print(i)
        resultVal.append(multiply(matrixA,matrixB,ip=start_ip,number=i))

    for i in range(len(resultVal)):
        if resultVal[i] != resultVal[0]:
            QoS = False
    file =open("results/results2.txt", "a")
    file.write(str(devices)+","+str(resultVal)+"\n")
    file.close()

def runTest3():
    sizes = [10, 100,1000,10000,100000]
    results = []
    resultString = "[accuracy, result], "
    for value in sizes:
        results.append([value, CalcPi(value)["result"]])
    #print(results)
    file =open("results/results3.txt", "a")
    file.write(resultString+", "+str(results)+"\n")
    file.close()

def runTest4(matrixA, matrixB):
    resultBase = localTime(matrixA, matrixB)
    resultOff = []
    input("\n Please change the resource allocation method on "+start_ip+" to even, then press any key to continue ...")
    resultOff.append(offTime(matrixA, matrixB))
    input("\n Please change the resource allocation method on "+start_ip+" to ready, then press any key to continue ...")
    resultOff.append(offTime(matrixA, matrixB))
    input("\n Please change the resource allocation method on "+start_ip+" to geo, then press any key to continue ...")
    resultOff.append(offTime(matrixA, matrixB))
    file =open("results/results4.txt", "a")
    file.write("correct output: "+str(resultOff)+"\n")
    file.close()

def runTest5(matrixA, matrixB):
    input("\n Please quit one of the device API's, then press any key to continue ...")

    resultBase = localTime(matrixA, matrixB)
    resultOff = offTime(matrixA, matrixB)
    #print(resultBase,resultOff)
    valid = False
    if (resultBase[0] == resultOff[0]):
        valid = True
    file =open("results/results5.txt", "a")
    file.write("correct output: "+str(valid)+"\n")
    file.close()

def main():
    # Create File:
    #file = open('results.txt', 'w')
    #file.write("Test Matrix size (num of rows), Time Locally, Time offloaded, Time offloaded with Distribution\n");
    #file.close()
    #popIps(start_ip)
    # EXP 1 (System Validation): Test with different sizes
    print("test 1: size of computation")
    runTest1(10)
    runTest1(20)
    runTest1(30)
    runTest1(40)
    runTest1(50)
    runTest1(60)
    runTest1(70)
    runTest1(80)
    runTest1(90)
    runTest1(100)

    # EXP 2 (System Scalability): # Test with number of devices.
    print("test 2: number of devices")
    runTest2(9) # Currently only have access to 9 devices.

    # EXP 3 (Computation Flexibility): # Test with different computations.
    print("test 3: Calc accuracy of Pi")
    runTest3()

    # Required matrices for 4 and 5
    matrix1 = createMatrix(10,1)
    matrix2 = createMatrix(10,1)

    # EXP 4 (Resource Allocation): # Test with different allocation methods
    print("test 4: allocation of resources")
    runTest4(matrix1, matrix2)

    # EXP 5 (Robustness): # Check system handling dropouts
    print("test 5: robustness of system")
    runTest5(matrix1,matrix2)

    #offResult = createMatrix(len(matrix1),0)
    #matrix1Temp = convMat(matrix2)
    #matrix2Temp = convMat(matrix1)
    # multiply
    # offResult = multiply(matrix1Temp, matrix2Temp, "192.168.1.15")
    #print(offResult)



if __name__ == "__main__":
    main()