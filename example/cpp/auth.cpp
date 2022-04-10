#include <string>
#include <tuple>
#include <cstdint>
#include <iostream>
#include <curl/curl.h>
#include <json/json.h>

typedef std::uint32_t u32;
typedef std::tuple<bool, std::string> CodeRes;

namespace test_auth {
    static std::string url("http://localhost:5000");
    static CURL *curl;
    static Json::Value root;
    static Json::Reader reader;
    static std::string data_buffer;
    static bool verbose_curl = true;

    static void init() {
        curl_global_init(CURL_GLOBAL_ALL);
        curl = curl_easy_init();
    }

    static size_t write_buffer(void *ptr, size_t size, size_t nmemb, std::string* data) {
        data->append((char*) ptr, size * nmemb);
        return size * nmemb;
    }

    static void clean() {
        curl_easy_cleanup(curl);
        curl_global_cleanup();
    }
    
    void init_curl_GET(std::string url) {
        curl_easy_setopt(curl, CURLOPT_URL, (url).c_str());
        curl_easy_setopt(curl, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_0);
        curl_easy_setopt(curl, CURLOPT_HTTPGET, 1L);
        curl_easy_setopt(curl, CURLOPT_FORBID_REUSE, 1L);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_buffer);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &data_buffer);
        curl_easy_setopt(curl, CURLOPT_VERBOSE, verbose_curl);
    }

    void init_curl_POST(std::string url) {
        curl_easy_setopt(curl, CURLOPT_URL, (url).c_str());
        curl_easy_setopt(curl, CURLOPT_HTTP_VERSION, CURL_HTTP_VERSION_1_0);
        curl_easy_setopt(curl, CURLOPT_HTTPPOST, 1L);
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_buffer);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &data_buffer);
        curl_easy_setopt(curl, CURLOPT_VERBOSE, verbose_curl);
    }

    static CodeRes get_code(std::string phone_number) {
        init();
        std::string req_string("/sendCode?phoneNumber=" + phone_number);
        init_curl_GET(url+req_string);

        CodeRes def = { false, std::string() };
        auto res = curl_easy_perform(curl);

        if(res != CURLE_OK) return def;

        bool parse_success;
        if((parse_success = reader.parse(data_buffer.c_str(), root))) {
            auto value = root.get("sentCode", "default").asString();
            std::cout << root << std::endl;
            return { parse_success, value };
        }

        clean();
        return def;
    };

    static bool confirm_code(std::string code, std::string code_hash) {
        std::string req_string("/signin");
        init_curl_POST(url+req_string);
        std::string body;

        body.append("{\"phoneNumber\":\"+393421323295\",");
        body.append("\"phoneCode\":");
        body.append(code);
        body.append(",");
        body.append("\"phoneCodeHash\":\"");
        body.append(code_hash + "\"}");

        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, body.c_str());

        auto res = curl_easy_perform(curl);
        clean();
        return res != CURLE_OK;
    }
}

int main(int argc, char** argv) {
    std::string code;
    std::string phone_number;
    std::cout << "Insert your telegram phone number (international format)..." << std::endl;
    std::cin >> phone_number;

    if(test_auth::verbose_curl) std::cout << "\n\nlibcurl verbosity enabled...\n\n" << std::endl;
    auto code_hash = std::get<1>(test_auth::get_code(phone_number));

    std::cout << code_hash << std::endl;
    std::cout << "Insert code sent by telegram..." << std::endl;
    std::cin >> code;
    bool ok = test_auth::confirm_code(code, code_hash);
    std::cout << (!ok ? "Done" : "Failed") << std::endl;
    return ok;
}
