# exit on error
set -e

rm -rf ./middle
rm -rf ./out-ios
rm -rf ./out-web

# parse markdown to html
cargo run

# modify html
python transform.py
