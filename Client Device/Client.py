# Python Web Client
import http.client, json, random, time, sys
from unittest import result

start_ip = "192.168.1.3"
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
def multiply(matrix1, matrix2, ip=start_ip):
    body = {
        "matrixA": matrix1, 
        "matrixB":matrix2
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

def offTime(matrix1, matrix2):
    offResult = createMatrix(len(matrix1),0)
    matrix1Temp = convMat(matrix2)
    matrix2Temp = convMat(matrix1)
    #start timer.
    start = time.time()
    # multiply
    offResult = multiply(matrix1Temp, matrix2Temp, "192.168.1.14")
    #stop timer.
    stop = time.time()
    print("Off Duration: ", stop-start)
    return [offResult,stop-start]

def singleOffTime(matrix1, matrix2):
    offResult = createMatrix(len(matrix1),0)
    matrix1Temp = convMat(matrix2)
    matrix2Temp = convMat(matrix1)
    #start timer.
    start = time.time()
    # multiply
    offResult = multiply(matrix1Temp, matrix2Temp, "192.168.1.15")
    #stop timer.
    stop = time.time()
    print("Off 1 Duration: ", stop-start)
    return [offResult,stop-start]

def runTest(size):
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
    resultMatrixOff1 = singleOffTime(matrixA, matrixB)
    # Perform offloading with proposed Architecture
    resultMatrixOff3 = offTime(matrixA, matrixB)
    #print(matrixA)
    #print(matrixB)
    #print(resultMatrixLocal)
    #print(resultMatrixOff)
    if(resultMatrixLocal[0] == resultMatrixOff3[0] and resultMatrixLocal[0] == resultMatrixOff1[0]):
        QoS = True
        print("All results are the same")
    file =open("results.txt", "a")
    file.write(str(size)+","+str(resultMatrixLocal[1])+","+str(resultMatrixOff1[1])+","+str(resultMatrixOff3[1])+","+str(QoS)+"\n")
    file.close()

def main():
    # Create File:
    #file = open('results.txt', 'w')
    #file.write("Test Matrix size (num of rows), Time Locally, Time offloaded, Time offloaded with Distribution\n");
    #file.close()
    # Test with different sizes
    #runTest(10)
    #runTest(20)
    #runTest(30)
    #runTest(40)
    #runTest(50)
    #runTest(60)
    #runTest(70)
    #runTest(80)
    #runTest(90)
    #runTest(100)
    matrix1 = createMatrix(100,1)
    matrix2 = createMatrix(100,1)
    offResult = createMatrix(len(matrix1),0)
    matrix1Temp = convMat(matrix2)
    matrix2Temp = convMat(matrix1)
    # multiply
    offResult = multiply(matrix1Temp, matrix2Temp, "192.168.1.15")
    print(offResult)



if __name__ == "__main__":
    main()