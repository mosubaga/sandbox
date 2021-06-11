import java.io.File

fun GetFileList() : MutableList<String>{
	val sPathName="[PATH]";
	val aFiles: MutableList<String> = mutableListOf()
	File(sPathName).walk().forEach {
		val sFile = it.toString();
		if ((sFile.contains(".py",ignoreCase=true)) || (sFile.contains(".pl",ignoreCase=true))){
			aFiles.add(sFile);
		}
	}
	return aFiles;
}

fun GetString(aFiles: MutableList<String>) {

	for (sFile in aFiles){
    	val lines: List<String> = File(sFile).readLines()
		val regex = "import".toRegex()

    	for(line in lines){
        	if (regex.containsMatchIn(line)){
        		print("[$sFile] : $line\n")
        	}
    	}
	}
}

fun main() {
	var aFiles = GetFileList();
	GetString(aFiles)
}

main();

