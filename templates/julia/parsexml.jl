using LightXML

# parse pom.xml
# xdoc is an instance of XMLDocument, which maintains a tree structure
xdoc = parse_file("pom.xml")

# get the root element
xroot = root(xdoc)  # an instance of XMLElement
# print its name
# println(name(xroot))  # this should print: bookstore

c = get_elements_by_tagname(xroot,"dependencies")

for d in child_nodes(c[1])
    if is_elementnode(d)
        e = XMLElement(d)
        for f in child_nodes(e)
            if name(f) == "artifactId"
                print(content(f))
                print("\n")
            end
        end
    end
end

#=
If the remainder of the script does not use the document or any of its children,
you can call free here to deallocate the memory. The memory will only get
deallocated by calling free or by exiting julia -- i.e., the memory allocated by
libxml2 will not get freed when the julia variable wrapping it goes out of
scope.
=#
free(xdoc)