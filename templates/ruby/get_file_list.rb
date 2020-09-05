pathname = '[Folder]'
file_list = Array.new
file_list = Dir.glob("**/*.*")

fh = File.open("[Output File List]","w")
file_list.each do |f|

# do whatever you want with f, which is a filename within the
# given directory (not fully-qualified)

  fh.write("#{f}\n")
end

fh.close
