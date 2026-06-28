#!/usr/bin/env sh
set -e

: "${DATABASE_URL:?DATABASE_URL not set}"

exec psql "$(echo "$DATABASE_URL" | sed -E 's#\+[a-z0-9]+://#://#')" "$@"
