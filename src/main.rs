extern crate soup;
extern crate pulldown_cmark;

use std::fs;
use std::error::Error;
use pulldown_cmark::{Parser, Options, html};

fn main() {
    println!("Hello there");

    let contents = fs::read_to_string("./basic.md")
      .expect("Something went wrong reading the file");
    // println!("Contents: {}", contents);

    let mut options = Options::empty();
    options.insert(Options::all());
    let parser = Parser::new_ext(&contents, options);

    let mut html_buf = String::new();
    html::push_html(&mut html_buf, parser);

    println!("HTML: {}", html_buf);

    fs::create_dir_all("./build");
    fs::write("./build/basic.html", html_buf).expect("Unable to write file");

}
