require 'nokogiri'
require 'pp'


def CleanString(string)

  string = string.sub(/^\s+/,"")
  string = string.sub(/\s+$/,"")
  string = string.gsub(/\s\s++/," ")

  return string
end



xlf_file = '[XLF file]'
xlf = File.open(xlf_file,"r:UTF-8")
doc = Nokogiri::XML(xlf)
xlf.close

# Remove all namespaces from the entire document
doc.remove_namespaces!

fout = File.new("rb_xlf.xml","w:UTF-8")
log = File.new("debug.log","w:UTF-8")

unit = doc.xpath('//file')

unit.each do |segment|
  text = segment.to_s
  file_text = "<root>\n" + text + "</root>\n"
  log.write(file_text)
  file_doc = Nokogiri::XML(file_text,nil,"UTF-8")
  trans_unit = file_doc.xpath('//trans-unit')
  trans_unit.each do |trans|
    trans = trans.to_s
    trans = trans.delete!("\n")

    if ((trans =~ /<source>(.+?)<\/source>/i) && ((trans =~ /<target>(.+?)<\/target>/i)))
      src = $1 if (trans =~ /<source>(.+?)<\/source>/i)
      tgt = $1 if (trans =~ /<target>(.+?)<\/target>/i)

      src = src.gsub!(/\<.+\>/,"")
      tgt = tgt.gsub!(/\<.+\>/,"")

      src_wordcount= src.to_s.split(" ").count
      tgt_wordcount= tgt.to_s.split(" ").count

      if ((src_wordcount >1) && (tgt_wordcount > 1))

        src = CleanString(src)
        tgt = CleanString(tgt)

        fout.write("#{src}\n")
        fout.write("#{tgt}\n\n")
      end
    end
  end
end

fout.close
log.close
