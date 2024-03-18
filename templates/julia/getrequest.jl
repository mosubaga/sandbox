using HTTP
using JSON

function get_request(sURL::String)

    try
        resp = HTTP.request("GET", sURL)
        respbody = String(resp.body)
        return respbody
    catch e
        println("Error: " + e)
    end
end

function parse_json(sBody::String)

    obj = JSON.parse(sBody)
    print(obj["[FIELD]"])

end

# ---- Main ------ #

sURL = "[URL]"
respbody = get_request(sURL)
parse_json(respbody)