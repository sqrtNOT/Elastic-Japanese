#!/bin/bash -x
curl -XDELETE -u elastic:$ELASTIC_PASS 'localhost:9250/jpnsearch'
curl -XPUT -u elastic:$ELASTIC_PASS 'localhost:9250/jpnsearch' -H 'Content-Type: application/json' -d '
{
	"settings": {
		"index": {
			"analysis": {
				"analyzer": {
					"kuromoji_normalize": {
						"type": "custom",
						"tokenizer": "kuromoji_tokenizer",
						"char_filter": [
							"icu_normalizer"
						],
						"filter": [
							"kuromoji_baseform",
							"kuromoji_part_of_speech",
							"cjk_width",
							"kuromoji_stemmer",
							"lowercase"
						]
					}
				}
			}
		}
	},
	"mappings": {
		"properties": {
			"document_id": {
				"type": "integer"
			},
			"sentence": {
				"type": "text",
				"analyzer": "kuromoji_normalize"
			}
		}
	}
}'


./elasticbulkloader.py
