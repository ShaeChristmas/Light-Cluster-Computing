const express = require("express");
const fs = require("fs");
var path = require("path");
const app = express();
var http = require("http");

// Is the device currently busy?
var busy = false;
var ips = require("./ips.json");

const port = 5000;

const bodyParser = require("body-parser");
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json());

function mutliplyMatrixAndDot(matrix, point) {
    // Found from https://developer.mozilla.org/en-US/docs/Web/API/WebGL_API/Matrix_math_for_the_web

    // Give a simple variable name to each part of the matrix, a column and row number
    let c0r0 = matrix[ 0], c1r0 = matrix[ 1], c2r0 = matrix[ 2], c3r0 = matrix[ 3];
    let c0r1 = matrix[ 4], c1r1 = matrix[ 5], c2r1 = matrix[ 6], c3r1 = matrix[ 7];
    let c0r2 = matrix[ 8], c1r2 = matrix[ 9], c2r2 = matrix[10], c3r2 = matrix[11];
    let c0r3 = matrix[12], c1r3 = matrix[13], c2r3 = matrix[14], c3r3 = matrix[15];
  
    // Now set some simple names for the point
    let x = point[0];
    let y = point[1];
    let z = point[2];
    let w = point[3];
  
    // Multiply the point against each part of the 1st column, then add together
    let resultX = (x * c0r0) + (y * c0r1) + (z * c0r2) + (w * c0r3);
  
    // Multiply the point against each part of the 2nd column, then add together
    let resultY = (x * c1r0) + (y * c1r1) + (z * c1r2) + (w * c1r3);
  
    // Multiply the point against each part of the 3rd column, then add together
    let resultZ = (x * c2r0) + (y * c2r1) + (z * c2r2) + (w * c2r3);
  
    // Multiply the point against each part of the 4th column, then add together
    let resultW = (x * c3r0) + (y * c3r1) + (z * c3r2) + (w * c3r3);
  
    return [resultX, resultY, resultZ, resultW];
}

function sendReq(ip,matrix, point) {
    var request = http.request(
        {
          host: ip,
          port: 5000,
          path: "/sendComp",
          method: "GET",
        },
        function (response) {
          var data = "";
          response.setEncoding("utf8");
          response.on("data", (chunk) => {
            data += chunk;
          });
          response.on("end", () => {
            res.end(data);
            console.log(data);
          });
        }
      );
      request.on("error", function (err) {
        console.log("error: Device " + ips[i] + " not found");
        console.log("error Message: " + err);
      });
      request.end();
}

function multiplyMatrices(matrixA, matrixB) {
    // Slice the second matrix up into rows
    let row0 = [matrixB[ 0], matrixB[ 1], matrixB[ 2], matrixB[ 3]];
    let row1 = [matrixB[ 4], matrixB[ 5], matrixB[ 6], matrixB[ 7]];
    let row2 = [matrixB[ 8], matrixB[ 9], matrixB[10], matrixB[11]];
    let row3 = [matrixB[12], matrixB[13], matrixB[14], matrixB[15]];
  
    // Multiply each row by matrixA FIX THIS SO THAT EACH ROW IS SENT TO AN INDIVIDUAL DEVICE
    let result0 = multiplyMatrixAndPoint(matrixA, row0);
    let result1 = multiplyMatrixAndPoint(matrixA, row1);
    let result2 = multiplyMatrixAndPoint(matrixA, row2);
    let result3 = multiplyMatrixAndPoint(matrixA, row3);
  
    // Turn the result rows back into a single matrix
    return [
      result0[0], result0[1], result0[2], result0[3],
      result1[0], result1[1], result1[2], result1[3],
      result2[0], result2[1], result2[2], result2[3],
      result3[0], result3[1], result3[2], result3[3]
    ];
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

// Get Device Information
app.get("/infoReq", (req, res) => {
  for (let i = 0; i < ips.length; i++) {
    console.log("Testing:" + ips[i]);
    var request = http.request(
      {
        host: ips[i],
        port: 5000,
        path: "/info",
        method: "GET",
      },
      function (response) {
        var data = "";
        response.setEncoding("utf8");
        response.on("data", (chunk) => {
          data += chunk;
        });
        response.on("end", () => {
          res.end(data);
          console.log(data);
        });
      }
    );
    request.on("error", function (err) {
      console.log("error: Device " + ips[i] + " not found");
      console.log("error Message: " + err);
    });
    request.end();
  }
});

// Request for Computation
app.get("/reqComp", (req, res) => {
  res.send([ip, !busy]);
  console.log([ip, !busy]);
});

// Validation of Computation
app.get("/compVal", async (req, res) => {
  ready = {};
  for (let i = 0; i < ips.length; i++) {
    var request = http.request(
      {
        host: ips[i],
        port: 5000,
        path: "/reqComp",
        method: "GET",
      },
      function (response) {
        var data = "";
        response.setEncoding("utf8");
        response.on("data", (chunk) => {
          data += chunk;
        });
        response.on("end", () => {
          res.end(data);
        });
      }
    );
    request.on("error", function (err) {
      console.log("error: Device " + ips[i] + " not found");
      console.log("error Message: " + err);
    });
    request.end();
  }
});

// Sending of Computation - Client recieving and sending.
app.get("/getComp", (req,res) => {
    try{
        multiplyMatrices(req.body.matrixA, req.body.matrixB);
    }catch{
        console.log("oops");
    }
});

// Receiving of Computation - Receiving from Master
app.get("/sendComp", (req,res) => {
    busy = true;
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
