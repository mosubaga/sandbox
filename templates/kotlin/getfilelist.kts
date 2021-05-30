import java.io.File


fun GetFileList(){
	val sPathName="[path]"
	File(sPathName).walk().forEach {
		val sFile = it.toString()
		if ((sFile.contains(".py",ignoreCase=true)) || (sFile.contains(".pl",ignoreCase=true))){
			print(sFile + "\n")
		}
	}
}

fun main() {
	GetFileList()
}

main()
