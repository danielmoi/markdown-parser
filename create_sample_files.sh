# for rsync, ensure that "/" is at the end so _contents_ are copied without parent folder
echo $MARKDOWN_ASSETS_PATH
echo $MARKDOWN_PARSER_PATH

# -a        Preserve permissions
# -v        Verbose
# --delete  Remove extraneous files from dest dirs

rsync -rv \
  $MARKDOWN_ASSETS_PATH/css \
  $MARKDOWN_PARSER_PATH/sample

rsync -rv \
  $MARKDOWN_ASSETS_PATH/js \
  $MARKDOWN_PARSER_PATH/sample
