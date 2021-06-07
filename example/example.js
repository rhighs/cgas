const FormData = require("form-data");
const fetch = require("node-fetch");
const fs = require("fs");

const url = "http://127.0.0.1:5000/user/+24131515154"

const uploadFile = async (filename, fileContent) => {
    fs.writeFile("./"+filename, fileContent, { flag: "wx" }, (err) => {
        if(err) throw err;
    });
    let stream = fs.createReadStream("./"+filename);
    let formData = new FormData();
    formData.append("file", stream, {
        contentType: "text/plain",
        name: "file",
        filename: filename
    })
    formData.append("mimeType", "text/plain", {
        contentType: "text/plain",
        name: "mimeType"
    })
    return await fetch(url + "/uploadFile", {
        method: "POST",
        body: formData
    }).then(async res => await res.json())
}

const downloadFile = async (uploadObject) => {
    let message = {
        message: uploadObject
    }
    return await fetch(url + "/downloadFile", {
        method: "POST",
        contentType: "application/json",
        body: message
    }).then(async res => await res.json())
}

(async () => {
    let obj = await uploadFile("x.txt", "some text data here");
    let final = await downloadFile(obj);
    console.log(final);
})();
