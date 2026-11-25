#!/bin/sh
# Тест art-uuid: формат, число строк, разбор версии
set -e
out=$(./art-uuid -r 3)
test "$(echo "$out" | grep -cE '^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$')" = 3
test "$(./art-uuid -p "$(./art-uuid -t)")" = "version 1 variant 1"
test "$(./art-uuid -p 00000000-0000-4000-8000-000000000000)" = "version 4 variant 1"
! ./art-uuid -p not-a-uuid 2>/dev/null
