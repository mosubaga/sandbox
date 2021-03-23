require 'nokogiri'

mt = File.open([XML_FILE])
doc = Nokogiri::XML(mt)
mt.close

print "Parsing ...\n\n"
fout_path = '[OUT_TXT]'
fout = File.new(fout_path,"w:utf-8")

doc.xpath('[SOME_XPATH]').each do |src|
  strsrc = src.text
  strsrc = strsrc.chomp
  fout.write("#{strsrc}\n")
end

fout.close
print "\nFinish parsing\n"

