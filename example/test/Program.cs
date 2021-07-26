using System;
using System.IO;
using System.Collections.Generic;
using System.Collections;
using System.Text;
using System.Text.Json;
using System.Net.Http;

namespace example
{
    class Program
    {
        static public string BASE_PATH = "./";
        static public string URL = "http://127.0.0.1:5000/user/+393421323295";
        static public string API_FILE_KEY = "file";

        static void Main(string[] args)
        {
            Console.Write("insert file name: ");
            var fileName = Console.ReadLine();
            Console.Write("insert file content(txt): ");
            var fileContent = Console.ReadLine();
            CreateFile(fileName, fileContent);
            var messageJson = SendFile(fileName);
            Console.WriteLine($"Uploaded file --> {messageJson}");
            var downloadMessage = DownloadFile(messageJson);
            Console.WriteLine($"Download result --> {downloadMessage}");
        }

        static string DownloadFile(string messageJson)
        {
            string message = $"{{ \"message\": {messageJson} }}";
            HttpContent jsonString = new StringContent(message, Encoding.UTF8, "application/json");
            using (var client = new HttpClient())
            {
                var resp = client.PostAsync(URL+"/downloadFile", jsonString).Result;
                return resp.Content.ReadAsStringAsync().Result;
            }
        }

        static void CreateFile(string fileName, string fileContent)
        {
            byte[] toWrite = Encoding.ASCII.GetBytes(fileContent);
            var f = new FileStream(BASE_PATH + fileName, FileMode.OpenOrCreate);
            f.Write(toWrite, 0, toWrite.Length);
            f.Close();
        }

        static string SendFile(string fileName)
        {
            Stream r = new FileStream(BASE_PATH + fileName, FileMode.Open);
            HttpContent content = new StreamContent(r);
            HttpContent mimeType = new StringContent("text/plain");
            using (var client = new HttpClient())
            using (var formData = new MultipartFormDataContent())
            {
                formData.Add(content, API_FILE_KEY, fileName);
                formData.Add(mimeType, "mimeType");
                var resp = client.PostAsync(URL + "/uploadFile", formData).Result;
                return resp.IsSuccessStatusCode ? resp.Content.ReadAsStringAsync().Result : "Error: upload unsuccessful";
            }
        }
    }
}
