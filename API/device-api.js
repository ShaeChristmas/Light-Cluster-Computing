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
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

function mutliplyMatrixAndDot(matrix, point) {
  // Found from https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/Matrix_math_for_the_web
  //console.log("multiplyMatrixAndDot: " + matrix);
  // Give a simple variable name to each part of the matrix, a column and row number
  size = Math.sqrt(matrix.length);
  console.log("Matrix: " + matrix[3 * size + 3]);
  console.log("Point: " + point);
  var returnRow = Array(size).fill(0);
  console.log("size: " + size);

  for (let i = 0; i < size; i++) {
    for (let j = 0; j < size; j++) {
      returnRow[i] += point[j] * matrix[size * i + j];
    }
  }
  return returnRow;
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
          valueToReturn = JSON.parse(data);
        } catch {
          reject(new Error(err));
        }
        console.log("data: " + eval(data)[1]);
        resolve({
          returnRow: eval(data)[1],
        });
      });
    });
    request.on("error", reject);
    request.write(postBody);
    request.end();
    //console.log("Outside: "+ JSON.stringify(request.end()));
  });
}

async function multiplyMatrices(matrixA, matrixB) {
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
  var nodev = ips.length;
  var count = 0;

  var promises = [];
  for (let i = 0; i < size; i++) {
    var point = new Array(size).fill(0);
    for (let j = 0; j < size; j++) {
      point[j] = matrixB[i + size * j];
    }
    // console.log("point: "+ point);
    // Async before the below function works, but its technically sequential.
    promises.push(
      sendReq(ips[i % nodev], matrixA, point).then((data) => {
        newMatrix[i] = data.returnRow;
        console.log(data.returnRow);
        count++;
        console.log(count);
      })
    );
  }
  await Promise.all(promises);
  // This code section is required, but i was wrapping it to try and make the code non-sequential.
  for (let i = 0; i < size; i++) {
    for (let j = 0; j < size; j++) {
      returnMatrix[i][j] = newMatrix[j][i];
    }
  }
  console.log(returnMatrix);
  return returnMatrix;
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
const { count } = require("console");
let name = info.name;
let ip = info.ip;
let mac = info.mac;
let computation = info.comp;
// Required Functions

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

// Get Device Information - not sure if will work with multiple devices.
app.get("/infoReq", async (req, res) => {
  promises = [];
  for (let i = 0; i < ips.length; i++) {
    promises.push(new Promise((resolve, reject) => {
      console.log("Testing:" + ips[i]);
      var request = http.request(
        {
          host: ips[i],
          port: 5000,
          path: "/info",
          method: "GET",
          timeout: 500
        },
      function (response) {
        var data = "";
        response.setEncoding("utf8");
        response.on("data", (chunk) => {
          data += chunk;
        });
        response.on("end", () => {
          res.end(data);
          resolve(data);
          //console.log(data);
        });
      }
      );
      request.on("timeout", () => {
        request.destroy();
      });
      request.on("error", function (err) {
        console.log("error: Device " + ips[i] + " not found");
        console.log("error Message: " + err);
        reject("Not found");
      });
      request.end();
    }));
    }

    return await Promise.allSettled(promises);
});

// Request for Computation Response
app.get("/reqComp", (req, res) => {
  res.send([ip, !busy]);
  console.log([ip, !busy]);
});

// Validation of Computation
app.get("/compVal", async (req, res) => {
  ready = {};
  promises = [];
  for (let i = 0; i < ips.length; i++) {
    promises.push(new Promise((resolve, reject) => {
      var request = http.request(
        {
          host: ips[i],
          port: 5000,
          path: "/reqComp",
          method: "GET",
          timeout: 500
        },
        function (response) {
          var data = "";
          response.setEncoding("utf8");
          response.on("data", (chunk) => {
            data += chunk;
          });
          response.on("end", () => {
            res.end(data);
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
      }))
    }
  return await Promise.allSettled(promises);
});

// Sending of Computation - Client recieving and sending.
app.get("/getComp", async function (req, res) {
  try {
    console.log("/getComp: This runnig");
    var result = await multiplyMatrices(req.body.matrixA, req.body.matrixB);
    console.log("/getComp output: \n" + result);
    res.send(result); //req.body.matrixA
  } catch (exception) {
    console.log("oops");
    console.log(exception);
  }
});

// Receiving of Computation - Receiving from Master
app.get("/sendComp", (req, res) => {
  busy = true;
  //console.log(req);
  var matrix = req.body.matrix;
  var point = req.body.point;
  var row = mutliplyMatrixAndDot(matrix, point);
  res.send([info.ip, row]);
  busy = false;
});

// Listen
app.listen(port, () => {
  console.log(`listening on port ${port}`);
  console.log(
    `info: \n name: ${name}\n ip: ${ip}\n mac: ${mac}\n Computation: ${computation}`
  );
});
