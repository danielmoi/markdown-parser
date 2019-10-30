# exit on error
set -e

rm -rf ./middle
rm -rf ./out-ios
rm -rf ./out-web

# transform
python transform-journals.py ios
python transform-journals.py web
