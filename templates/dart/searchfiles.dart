import 'dart:io';

// ---------------------------------------------------------------
void main() 
// ---------------------------------------------------------------
{
  String directoryPath = '[Folder_Name]';
  String keyword = "KEYWORD";

  var filelist = listFiles(Directory(directoryPath));

  for (String sFile in filelist)
  {
    ReadFileAsLines(sFile, keyword);
  }
}

// ---------------------------------------------------------------
List<String> listFiles(Directory dir) 
// ---------------------------------------------------------------
{

  List<String> filelist = [];

  if (dir.existsSync()) {
    dir.listSync(recursive: true).forEach((FileSystemEntity entity) {
      // Check if it's a File
      if (entity is File) {
        String pathname = entity.path;
        if ((pathname.endsWith(".py")) | (pathname.endsWith(".pl")))
        {
            // print('File: ${entity.path}');    
            filelist.add(pathname);
        }
      }
    });
  } else {
    print('Directory does not exist.');
  }

  return filelist;
}

// ---------------------------------------------------------------
void ReadFileAsLines(String filename, String keyword) 
// ---------------------------------------------------------------
{

  // Read the file line by line
  int i = 0;
  File file = File(filename);
  file.readAsLines().then((List<String> lines) {
    List<String> linesList = lines.toList();
    
    linesList.forEach((line) {
      i++;
      if (line.contains(keyword)){
        var lineout = line.trim();
        print('$filename [$i] : $lineout');
      }
    });
  }).catchError((e) {
    print('Error reading file: $e');
  });
}