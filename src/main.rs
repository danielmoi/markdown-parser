extern crate soup;
extern crate pulldown_cmark;
extern crate walkdir;

use std::fs;
use pulldown_cmark::{Parser, Options, html};
use walkdir::WalkDir;
use std::path::{Path, PathBuf, Component};
use std::ffi::OsStr;

fn main() {
    println!("Starting parser");

    let header_contents = fs::read_to_string("header.html").unwrap();

    let footer_contents = fs::read_to_string("footer.html").unwrap();

    for entry in WalkDir::new("documents") {
      let entry = entry.unwrap();
      let entry_path = Path::new(entry.path());

      // println!("entry_path: {:?}", entry_path);

      let mut new_entry_path = PathBuf::from("./");
      for component in entry_path.components() {
        if component == Component::Normal(OsStr::new("documents")) {
          new_entry_path.push("out");
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

        let contents = fs::read_to_string(entry_path)
          .expect("Error reading entry file");

        let mut options = Options::empty();
        options.insert(Options::all());
        let parser = Parser::new_ext(&contents, options);

        let mut html_buf = String::new();
        html_buf.push_str(&header_contents);
        html::push_html(&mut html_buf, parser);
        html_buf.push_str(&footer_contents);

        // TODO: Add details/summary with kuchiki / other

        let with_extension = new_entry_path.with_extension("html");

        fs::write(with_extension, html_buf).expect("Error writing to html");
      }
    }

    println!("Finished parsing");
}
