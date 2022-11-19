#include "boost/filesystem.hpp"
#include <iostream>

int main () {
for ( boost::filesystem::recursive_directory_iterator end, dir("[direcory]");
  dir != end; ++dir ) {
  std::cout << *dir << "\n";  // full path
  // std::cout << dir->path().filename() << "\n"; // just last bit
}
