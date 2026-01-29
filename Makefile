SITE_DIR := site
R2_BUCKET := R2:planogolny-wroclaw-pl

all: build sync purge

.PHONY: all build serve clean sync purge

build:
	mkdocs build

serve:
	mkdocs serve

clean:
	rm -rf $(SITE_DIR)

sync: build
	rclone sync ./$(SITE_DIR)/ $(R2_BUCKET) --progress

purge:
	curl -X POST "https://api.cloudflare.com/client/v4/zones/${CF_ZONE_ID}/purge_cache" \
		-H "Authorization: Bearer ${CF_API_TOKEN}" \
		-H "Content-Type: application/json" \
		--data '{"purge_everything":true}'
