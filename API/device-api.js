const express = require("express");
const fs = require("fs");
var path = require("path");
const app = express();
var http = require("http");
const querystring = require("query-string");

// Is the device currently busy?
var busy = false;
var ips = require("./ips.json");
//var matricies = require("./mats.json");

const port = 5000;

const bodyParser = require("body-parser");
app.use(bodyParser.json({ parameterLimit: 1000000, limit: "50mb" }));
app.use(
  bodyParser.urlencoded({
    parameterLimit: 1000000,
    limit: "50mb",
    extended: true,
  })
);

function multiplyMatrixAndDot(matrix, point) {
  // Found from https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/Matrix_math_for_the_web
  //console.log("multiplyMatrixAndDot: " + matrix);
  // Give a simple variable name to each part of the matrix, a column and row number
  size = Math.sqrt(matrix.length);
  //console.log("Matrix: " + matrix[3 * size + 3]);
  //console.log("Point: " + point);
  var returnRow = Array(size).fill(0);
  //console.log("size: " + size);
  points = point.split(",");
  //console.log(returnRow);
  for (let i = 0; i < size; i++) {
    for (let j = 0; j < size; j++) {
      //console.log(points[j]);
      returnRow[i] += points[j] * matrix[size * j + i];
    }
    //console.log("Return value: ", returnRow[i]);
  }
  //console.log(returnRow);
  return returnRow;
}

async function multiplyMatricesLocal(matrixA, points) {
  // iterate rows of matrixA
  size = Math.sqrt(matrixA.length);
  //console.log("Matrix 1: " + matrixA);
  //console.log("Matrix 2: " + matrixB);
  matrixResult = [];
  //console.log("Length: ", points.length);
  for (let i = 0; i < points.length; i++) {
    //console.log("MatrixA: " + matrixA);
    //console.log("Point: ", points[i]);
    matrixResult[i] = multiplyMatrixAndDot(matrixA, points[i]);
  }
  //console.log(matrixResult);
  return matrixResult;
}

function sendReq(ip, matrix, point) {
  return new Promise((resolve, reject) => {
    //console.log("sendReq: "+ ip+ ' '+matrix)
    var body = {
      matrix: matrix,
      point: point,
    };
    //console.log("vorkin?");
    var postBody = querystring.stringify(body);
    var options = {
      host: ip,
      port: 5000,
      path: "/sendComp",
      method: "GET",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": postBody.length,
      },
    };
    var request = http.request(options, function (response) {
      valueToReturn = null;
      var data = "";
      response.setEncoding("utf8");
      response.on("data", (chunk) => {
        data += chunk;
        return data;
      });
      response.on("end", () => {
        try {
          console.log("Function Ends");
          valueToReturn = JSON.parse(data);
          //console.log("Value to return: " + valueToReturn);
        } catch {
          reject(new Error(err));
        }
        resolve({
          returnRow: eval(data)[1],
        });
        //console.log("data: " + eval(data)[1]);
      });
    });
    request.on("error", reject([0,ip,point]));
    request.write(postBody);
    request.end();
    //console.log("Outside: "+ JSON.stringify(request.end()));
  });
}

function sendReqPi(ip, min, max) {
  return new Promise((resolve, reject) => {
    //console.log("sendReq: "+ ip+ ' '+matrix)
    var body = {
      min: min,
      max: max
    };
    //console.log("vorkin?");
    var postBody = querystring.stringify(body);
    var options = {
      host: ip,
      port: 5000,
      path: "/sendComp",
      method: "GET",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
        "Content-Length": postBody.length,
      },
    };
    var request = http.request(options, function (response) {
      valueToReturn = null;
      var data = "";
      response.setEncoding("utf8");
      response.on("data", (chunk) => {
        data += chunk;
        return data;
      });
      response.on("end", () => {
        try {
          valueToReturn = JSON.parse(data);
          //console.log("Value to return: " + valueToReturn);
        } catch {
          reject(new Error(err));
        }
        resolve({
          value: eval(data)[1],
        });
        //console.log("data: " + eval(data)[1]);
      });
    });
    request.on("error", reject);
    request.write(postBody);
    request.end();
    //console.log("Outside: "+ JSON.stringify(request.end()));
  });
}

async function multiplyMatrices(matrixA, matrixB, number = 0) {
  // Check matrices size.
  size = Math.sqrt(matrixA.length);
  //console.log(size);
  // Search through Rows.
  var newMatrix = Array(size)
    .fill(0)
    .map(() => Array(size).fill(0));
  var returnMatrix = Array(size)
    .fill(0)
    .map(() => Array(size).fill(0));
  //console.log(newMatrix);
  if (number == 0) {
    var nodev = ips.length;
  } else {
    var nodev = number;
  }

  var promises = [];
  var points = [];
  for (let i = 0; i < size; i++) {
    var point = new Array(size).fill(0);
    for (let j = 0; j < size; j++) {
      point[j] = matrixB[j + size * i];
    }
    points.push(point);
    // console.log("point: "+ point);
    // Async before the below function works, but its technically sequential.
  }
  newMatrix = [];
  // Decide new rows to send to multiplyMatricesLocal.
  num = points.length;
  amount = Math.ceil(num / nodev);
  //console.log("Amount: ", amount);
  var curcount = 0;
  for (let i = 0; i <= nodev - 1; i++) {
    pointsToUse = points.slice(curcount, curcount + amount);
    curcount += amount;

    //console.log("Points: ", pointsToUse);
    // Set each as promise
    promises.push(
      sendReq(ips[i], matrixA, pointsToUse).then((data) => {
        for (let j = 0; j < data.returnRow.length; j++) {
          newMatrix[i * amount + j] = data.returnRow[j];
        }
      })
    );
  }
  pointsToUse = points.slice(curcount, points.length);
  //console.log("Points: ", pointsToUse);
  // Set each as promise
  if (pointsToUse.length > 0) {
    promises.push(
      sendReq(ips[nodev], matrixA, pointsToUse).then((data) => {
        //console.log("SendReq Data: ",data);
        for (let i = 0; i < data.returnRow.length; i++) {
          newMatrix[(nodev - 1) * amount + i] = data.returnRow[i];
        }
      })
    );
  }
  await Promise.all(promises);
  for (let i =0; i< promises.length;i++) {
    console.log(promises[i]);
  }
  //console.log("Returning Matrix: ",newMatrix);
  return newMatrix;
}

async function PiLocal(min, max) {
  //console.log("min: ",typeof min," max: ",typeof max);
  result = 0;
  for (let n = parseInt(min)+1; n <= parseInt(max); n += 4) {
    result += 4 / (n * (n + 1) * (n + 2));
    result -= 4 / ((n+2) * (n + 3) * (n + 4));
  }
  //console.log("result: ", result);
  return result;
}

async function calcPi(Accuracy, number = 0) {
  //console.log("Running Pi Calculation with Accuracy: ", Accuracy, ", Number: ", number);
  reps = Accuracy; // Hangs at 1000000000
  result = 3;
  if (number == 0) {
    var nodev = ips.length;
  } else {
    var nodev = number;
  }
  body = {};
  promises = [];
  if (nodev == 1) {
    op = 1;
    n = 2;
    for (let n = 2; n <= 2 * reps + 1; n += 2) {
      result += 4 / (n * (n + 1) * (n + 2) * op);
      op *= -1;
    }
    //console.log("Result: ", result);
    return { result: result.toString().replace(/(\.0*|(?<=(\..*))0*)$/, "") };
  } else {
    perdev = reps / nodev;
    n = 2;
    resultToSend = 0;
    for (let i = 0; i < nodev; i++) {
      //console.log("sending to node: ", ips[i]);
      promises.push(sendReqPi(ips[i],i * perdev + 1, (i + 1) * perdev + 1).then((data) => {
          resultToSend += data.value;
        }));
    }
    await Promise.all(promises);
    resultToSend +=3;
    return { result: resultToSend.toString().replace(/(\.0*|(?<=(\..*))0*)$/, "") };
  }
}

app.use(function (req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header(
    "Access-Control-Allow-Headers",
    "Origin, X-Requested-With, Content-Type, Accept"
  );
  next();
});

// Required Info
var info = require("./local.json");
let name = info.name;
let ip = info.ip;
let mac = info.mac;
let computation = info.comp;

// Ask for Device Info
app.get("/info", (req, res) => {
  // Filepath
  var options = {
    root: path.join(__dirname),
  };
  var filename = "local.json";
  res.sendFile(filename, options, function (err) {
    if (err) {
      next(err);
    } else {
      console.log("Sent:", filename);
    }
  });
});

function reqInfo(ip) {
  return new Promise((resolve, reject) => {
    //console.log("Testing:" + ip);
    var request = http.request(
      {
        host: ip,
        port: 5000,
        path: "/info",
        method: "GET",
        timeout: 500,
      },
      function (response) {
        var data = "";
        response.setEncoding("utf8");
        response.on("data", (chunk) => {
          data += chunk;
        });
        response.on("end", () => {
          //res.end(data);
          resolve(data);
          //console.log(data);
        });
      }
    );
    request.on("timeout", () => {
      request.destroy();
    });
    request.on("error", function (err) {
      console.log("error: Device " + ip + " not found");
      console.log("error Message: " + err);
      reject("Not found");
    });
    request.end();
  });
}

// Get Device Information - not sure if will work with multiple devices.
app.get("/infoReq", async (req, res) => {
  values = [];
  promises = [];
  for (let i = 0; i < ips.length; i++) {
    promises.push(
      reqInfo(ips[i]).then((data) => {
        //console.log("Data: "+data);
        values[i] = data;
      })
    );
  }
  await Promise.all(promises);
  //console.log("Values: "+values);
  res.send(values);
});

// Request for Computation Response
app.get("/reqComp", (req, res) => {
  res.send([ip, !busy]);
  console.log([ip, !busy]);
});

// RequestComp
function reqComp(ip) {
  return new Promise((resolve, reject) => {
    var request = http.request(
      {
        host: ip,
        port: 5000,
        path: "/reqComp",
        method: "GET",
        timeout: 500,
      },
      function (response) {
        var data = "";
        response.setEncoding("utf8");
        response.on("data", (chunk) => {
          data += chunk;
        });
        response.on("end", () => {
          //res.end(data);
          resolve(data);
        });
      }
    );
    request.on("timeout", () => {
      request.destroy();
    });
    request.on("error", function (err) {
      console.log("error: Device " + ips[i] + " not found");
      console.log("error Message: " + err);
      reject("Not Found");
    });
    request.end();
  });
}

// Validation of Computation
app.get("/compVal", async function (req, res) {
  ready = [];
  promises = [];
  for (let i = 0; i < ips.length; i++) {
    promises.push(
      reqComp(ips[i]).then((data) => {
        //console.log("Data: "+ data);
        ready[i] = data;
      })
    );
  }
  await Promise.all(promises);
  //console.log("Ready: "+ready);
  res.send(ready);
});

// Sending of Computation - Client recieving and sending.
app.get("/getComp", async function (req, res) {
  try {
    //console.log("/getComp: This runnig");
    //console.log(req)
    if (req.body.matrixA != null) {
      var result = await multiplyMatrices(
        req.body.matrixA,
        req.body.matrixB,
        req.body.number
      );
    } else if (req.body.accuracy != null) {
      //console.log("Identified as Pi Calculation");
      var result = await calcPi(req.body.accuracy, req.body.number);
    } else {
      var result = { error: "No calculation found" };
    }
    res.send(result); //req.body.matrixA
    //console.log("/getComp output: \n" + result);
  } catch (exception) {
    console.log("oops");
    console.log(exception)
  }
});

// Receiving of Computation - Receiving from Master
app.get("/sendComp", (req, res) => {
  if (req.body.matrix != null) {
    busy = true;
    //console.log(req);
    var matrix = req.body.matrix;
    var points = req.body.point;
    var rows = [];
    multiplyMatricesLocal(matrix, points).then((data) => {
      rows = data;
      console.log("Row outputs: ",rows);
      res.send([info.ip, rows]);
      busy = false;
    });
  } else if (req.body.min != null) {
    //console.log("Identified as Pi Calculation in /sendComp");
    busy = true;
    var min = req.body.min;
    var max = req.body.max;
    //console.log(req);
    PiLocal(min, max).then((data) => {
      value = data;
      //console.log("value output: ", value);
      res.send([info.ip, value]);
      busy = false;
    });
  }
});

// Listen
app.listen(port, () => {
  console.log(`listening on port ${port}`);
  console.log(
    `info: \n name: ${name}\n ip: ${ip}\n mac: ${mac}\n Computation: ${computation}`
  );
});
