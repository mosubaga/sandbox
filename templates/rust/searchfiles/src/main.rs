use std::fs::{self, File};
use std::io::{self, Write, BufRead};
use std::path::{Path, PathBuf};

fn main() -> io::Result<()> {
    let result_log = "result.log";
    let root_dir = "[Path_to_file]";
    let keyword = "[Keyword]";

    let mut out_file = File::create(result_log)?;

    println!("Getting files from {} ..", root_dir);
    let file_list = get_file_list(root_dir)?;

    for file in file_list {
        let lines = read_file_lines(&file)?;

        let mut line_num = 1;
        for line in lines {
            if line.contains(keyword) {
                write!(out_file, "{} ({}): {}\n", file.display(), line_num, line).expect("Cannot write to file!!");
                println!("{} ({}): {}", file.display(), line_num, line);
            }
            line_num += 1;
        }
    }

    println!("-- Scan complete --");
    Ok(())
}

fn get_file_list(root: &str) -> io::Result<Vec<PathBuf>> {
    let mut file_list = Vec::new();
    visit_dirs(Path::new(root), &mut |file_path| {
        if let Some(file_name) = file_path.file_name() {
            if let Some(file_name_str) = file_name.to_str() {
                if file_name_str.ends_with(".py") || file_name_str.ends_with(".pl") {
                    file_list.push(file_path.to_path_buf());
                }
            }
        }
        Ok(())
    })?;
    Ok(file_list)
}

fn read_file_lines(file_path: &Path) -> io::Result<Vec<String>> {
    let file = File::open(file_path)?;
    let reader = io::BufReader::new(file);
    let lines: Vec<String> = reader.lines().collect::<Result<_, _>>()?;
    Ok(lines)
}

fn visit_dirs(dir: &Path, callback: &mut dyn FnMut(&Path) -> io::Result<()>) -> io::Result<()> {
    if dir.is_dir() {
        for entry in fs::read_dir(dir)? {
            let entry = entry?;
            let path = entry.path();
            if path.is_dir() {
                visit_dirs(&path, callback)?;
            } else {
                callback(&path)?;
            }
        }
    }
    Ok(())
}
