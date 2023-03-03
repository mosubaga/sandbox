extern crate walkdir;
use walkdir::WalkDir;

fn main() {

    let spath = "[ROOTDIR]";
    for file in WalkDir::new(spath).into_iter().filter_map(|file| file.ok()) {
        let sfilename = file.path().display().to_string();

        if sfilename.ends_with(".js"){
            println!("{}", sfilename);
        }
    }
}