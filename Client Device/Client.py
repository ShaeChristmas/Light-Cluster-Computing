# Python Web Client
import http.client
import json

ips = []
ready = []
matrixTest = [1]
matrixC = [1,2,3,4,5,6,7,8,9]
matrixID = [1,0,0,0,1,0,0,0,1]
matrixD = [2,4,6,8,10,12,14,16,18]
matrixResult = []

headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept",
    "Content-Type": "application/json"
}


def popIps(ip):
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
        print(valueToAdd)
    connection.close()

def readyCheck():
    # Create a connection to the server
    connection = http.client.HTTPConnection("localhost", 5000)
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

def multiply(matrix1, matrix2):
    body = {
        "matrixA": matrix1, 
        "matrixB":matrix2
    }
    JSONbody = json.dumps(body).encode()
    #print(JSONbody)
    # Create a connection to the server
    connection = http.client.HTTPConnection("localhost", 5000)
    # Send a request to the server
    connection.request('GET', '/getComp',body=JSONbody,headers=headers)
    # Read the response from the server
    response = connection.getresponse()
    # Decode the response
    data = response.read().decode()
    data = json.loads(data)
    #print(data)
    return data

def main():
    matrixResult = []
    # Print ips before
    print("Before: "+str(ips))
    # Populate ips
    popIps("localhost")
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
    matrixResult = multiply(matrixC, matrixID)
    # Print result matrix after calculation
    print("Result Matrix: "+str(matrixResult))
    # Reset Result Matrix
    matrixResult = []
    # Print result matrix before calculation
    print("Result Matrix: "+str(matrixResult))
    # Multiply MatrixA and MatrixID
    matrixResult = multiply(matrixC, matrixD)
    # Print result matrix after calculation
    print("Result Matrix: "+str(matrixResult))

if __name__ == "__main__":
    main()