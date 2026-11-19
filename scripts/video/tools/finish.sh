#!/bin/bash
# usage: finish.sh film  -> full render + sfx + mix
V=/tmp/claude-0/-home-user-osn-geografi/94d8461e-73a7-5f3c-8634-0bdceec582c0/scratchpad/video
S=/root/.claude/plugins/synced/5c6bea52-a78a-42c6-b441-08b1fdd4d4a0_7324d7bd-5b25-425a-96ab-a100ca9297cc/d92346f7-5140-4ddb-b284-a3b42995e5b0/skills/motion-reel/scripts
cd $V && mkdir -p out/$1 && (timeout 3500 node $S/render.mjs --film $1 --video-only --fps 30 --workers 4 && node $S/sfx.mjs $1 && node $S/mix.mjs $1 --music-db -10 --sfx-db -4 --vo-db 3) > out/$1/render.log 2>&1; echo "EXIT $?" >> out/$1/render.log
