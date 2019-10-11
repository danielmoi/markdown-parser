extern crate soup;
extern crate pulldown_cmark;
extern crate walkdir;
extern crate filetime;

use std::fs;
use pulldown_cmark::{Parser, Options, html};
use walkdir::WalkDir;
use std::path::{Path, PathBuf, Component};
use std::ffi::OsStr;
use filetime::FileTime;

fn main() {
    let SOURCE_DIR = "in";
    let TARGET_DIR = "middle";

    println!("Starting parser");

    for entry in WalkDir::new(SOURCE_DIR) {
      let entry = entry.unwrap();
      let entry_path = Path::new(entry.path());

      // println!("entry_path: {:?}", entry_path);

      let mut new_entry_path = PathBuf::from("./");
      for component in entry_path.components() {
        if component == Component::Normal(OsStr::new(SOURCE_DIR)) {
          new_entry_path.push(TARGET_DIR);
        }
        else {
          new_entry_path.push(component);
        }
      }

      if entry_path.is_dir() {
        fs::create_dir_all(new_entry_path)
          .expect("Error creating directory");
        continue;
      }

      if entry_path.is_file() {
        // println!("entry_path {:?}", entry_path);
        // println!("new_entry_path {:?}", new_entry_path);

        let ext = entry_path.extension();

        // don't copy files without an extension
        match ext {
          None => continue,
          _ => (),
        }

        // just copy if not markdown (no parsing required)
        if (ext.unwrap() != "md") {
          fs::copy(entry_path, new_entry_path)
            .expect("Error copying file");
          continue;
        }

        let metadata = fs::metadata(entry_path);


        // parse markdown
        let contents = fs::read_to_string(entry_path)
          .expect("Error reading entry file");

        let mut options = Options::empty();
        options.insert(Options::all());
        let parser = Parser::new_ext(&contents, options);

        let mut html_buf = String::new();
        html::push_html(&mut html_buf, parser);

        // TODO: Add details/summary with kuchiki / other

        let with_extension = new_entry_path.with_extension("html");

        // TODO: is there a way to re-use the path with_extension?
        let path_copy = Path::new(&with_extension).to_path_buf();

        fs::write(with_extension, html_buf).expect("Error writing to html");


        // TODO: set ctime too (in addition to modified and access times)
        let rs_timestamp = FileTime::from_last_modification_time(&metadata.unwrap());
        filetime::set_file_times(path_copy, rs_timestamp, rs_timestamp).unwrap();
      }
    }

    println!("Finished parsing");
}
