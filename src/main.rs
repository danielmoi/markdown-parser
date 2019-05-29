extern crate soup;
extern crate pulldown_cmark;
extern crate walkdir;
extern crate kuchiki;

use std::fs;
use pulldown_cmark::{Parser, Options, html};
use walkdir::WalkDir;
use std::path::Path;
use kuchiki::traits::*;

fn main() {
    println!("Starting parser");

    let out = Path::new("./out");

    let header_contents = fs::read_to_string("header.html").unwrap();

    let footer_contents = fs::read_to_string("footer.html").unwrap();



    for entry in WalkDir::new("documents") {
      let entry = entry.unwrap();
      let entry_path = Path::new(entry.path());

      let parent = entry_path.parent().unwrap();
      let new_parent_path = out.join(parent);

      fs::create_dir_all(&new_parent_path)
        .expect("Error creating directory");

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

        let html_str = html_buf.clone();

        // Add details/summary
        let document = kuchiki::parse_html().one(html_str);
        let css_selector = "h2";

        let magic = document.select(css_selector).unwrap();
        println!("---------------");
        println!("magic.size {}", magic.count());

        for css_match in document.select(css_selector).unwrap() {
          println!("in the for....");
          let as_node = css_match.as_node();
          // let new = kuchiki::NodeRef::new_element("div", []);
          // as_node.append(new);
          println!("NODE: {:#?}", as_node.to_string());
//           as_node.detach().borrow();
            // println!("NODE: {:#?}", as_node.to_string());
        }
          println!("document: {:#?}", &document.to_string());

        let new_entry_path = out.join(&entry_path).with_extension("html");

        fs::write(new_entry_path, document.to_string()).expect("Error writing to html");
        // fs::write(new_entry_path, html_buf).expect("Error writing to html");
      }
    }

    println!("Finished parsing");
}
