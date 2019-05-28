extern crate soup;
extern crate pulldown_cmark;
extern crate walkdir;

use std::fs;
use std::error::Error;
use pulldown_cmark::{Parser, Options, html};
use walkdir::WalkDir;
use std::path::Path;

fn main() {
    println!("Hello there");

    let out = Path::new("./out");

    for entry in WalkDir::new("documents") {
      println!("--------------");
      let entry = entry.unwrap();
      // println!("entry: {}", entry.metadata());
      println!("entry: {}", entry.path().display());

      let entry_path = Path::new(entry.path());
      println!("entry_path: {}", entry_path.display());
      let parent = entry_path.parent().unwrap();
      println!("parent: {}", parent.display());

      let new_parent_path = out.join(parent);
      println!("new_parent_path: {}", &new_parent_path.display());
      fs::create_dir_all(&new_parent_path);

      let is_file = entry_path.is_file();
      println!("is_file: {}", is_file);

      if (entry_path.is_file()) {

        let contents = fs::read_to_string(entry_path)
          .expect("Something went wrong reading the file");
        // println!("Contents: {}", contents);

        let mut options = Options::empty();
        options.insert(Options::all());
        let parser = Parser::new_ext(&contents, options);

        let mut html_buf = String::new();
        html::push_html(&mut html_buf, parser);


        let new_entry_path = out.join(entry_path);
        println!("new_entry_path: {}", &new_entry_path.display());
        fs::write(new_entry_path, html_buf).expect("Fail.......");
      }
    }



    // println!("HTML: {}", html_buf);

    // let parent_folder = file.parent();
    // println!("parent_folder: {}", parent_folder);
    // fs::create_dir_all("./build");
    // fs::write("./build/basic.html", html_buf).expect("Unable to write file");

}
