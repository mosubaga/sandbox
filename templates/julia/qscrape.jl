using HTTP
using JSON
using Cascadia
using Gumbo

function get_request(sURL::String)
    try
        resp = HTTP.request("GET", sURL)
        respbody = String(resp.body)
        return respbody
    catch e
        println("Error: " + e)
    end
end

function parse_html(html_content::String)

    # Parse the HTML content
    parsed_document = parsehtml(html_content)

    table = eachmatch(sel"tbody",parsed_document.root)
    items = eachmatch(sel"tr",table[1])

    for x in items
        e = x[2][1]
        
        # Sometimes it picks up header even if you do not intend to
        if typeof(e) !== HTMLText
            println(e[1])
        end
    end
end

# ---- Main ------ #

sURL = "URL"
respbody = get_request(sURL)
parse_html(respbody)