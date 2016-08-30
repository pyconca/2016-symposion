STATIC_ROOT ?= "./symposion2016/static"

.PHONY: install-deps test-less-deps site.css

default: site.css

site.css: test-less-deps
	$(MAKE) -C $(STATIC_ROOT)/symposion2016 build

test-less-deps:
	@if ! which uglifyjs; then echo "-ERROR- Missing UglifyJS. Please run: npm install -g uglify-js"; exit 1; fi
	@if ! which lessc; then echo "-ERROR- Missing Less. Please run: npm install -g less"; exit 1; fi

install-deps:
	npm install -g uglify-js less
