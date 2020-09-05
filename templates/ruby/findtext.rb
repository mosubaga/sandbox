
srcfile = "[IN]"
tgtfile = "[OUT]"

fsrc = File.open(srcfile,"r:utf-8")
ftgt = File.open(tgtfile,"w:utf-8")

while (srcline = fsrc.gets)
   if (srcline =~ /&Text/i)
      ftgt.write(srcline)
   end
end

fsrc.close
ftgt.close
