using Printf

function list_files_recursive(directory::String, file_list::Vector{String}=String[])
    items = readdir(directory)
    re = r"\.(py|pl|rb|cpp|go)$"
    for item in items
        path = joinpath(directory, item)
        if isdir(path)
            file_list = list_files_recursive(path, file_list)
        else
            if (occursin(re,item))
                push!(file_list, path)
            end
        end
    end
    return file_list
end

function read_file_lines(filename::AbstractString, lines::Vector{String}=String[])
    # lines = String[]  # Initialize an empty array to store lines
    
    # Open the file
    open(filename, "r") do file
        # Read each line and append it to the array
        for line in eachline(file)
            push!(lines, line)
        end
    end
    
    return lines
end

# --- Main --- #

key = "[KEY]"
directory_path = "[PATH]"
files = list_files_recursive(directory_path)
for file in files
    i = 0
    lines = read_file_lines(file)
    for line in lines
         i+=1
        trimmedline = strip(line)
        if (occursin(key,trimmedline))
            @printf("[%s:%d] %s\n", file, i, trimmedline)
        end
    end
end


