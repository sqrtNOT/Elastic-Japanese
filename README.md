# Elastic-Japanese
Fast retrieval of example sentences for Japanese learners using common crawl data and elasticsearch

In order to get this working you need a few things set up first.
1. An elasticsearch node running on localhost on port 9250.
2. An 'elastic' user account on that server with permissions to write data.
3. An environment variable ELASTIC_PASS that contains your elasticsearch credentials in the form: "elastic:password" On linux this can be accomplished with `export ELASTIC_PASS='elastic:password'` in your shell or in ~/.bashrc if you want it to be permanent.
4. Kuromoji and icu installed on your elasticsearch node. `elasticsearch-plugin install analysis-kuromoji` and `elasticsearch-plugin install analysis-icu` to install them but make sure to check the documentation for backwards compatibility considerations or if you need an analyzer for a language other than Japanese: https://www.elastic.co/guide/en/elasticsearch/plugins/current/analysis.html
5. A local copy of the cc-100 dataset downloaded from https://data.statmt.org/cc-100/ or huggingface at /datasets/cc-100/ja.txt. Other languages and file locations will likely work but have not been tested and require modifying the path sent to chunkparsecc100. If you'd like to use a different data set then replace the parsecc100 function and calls to it with your own. Documents should be returned one at a time in full and sentences separated by newlines.
6. Run deleteandload.sh to setup the elasticsearch index and start loading the data. You may also want to change the chunk size from 64MiB to something else as this was optimized for a specific machine.
