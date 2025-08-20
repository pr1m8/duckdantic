#!/bin/bash
set -euo pipefail

LIST_FILE="$1"
GROUP="${2:-dev}"

if [[ ! -f $LIST_FILE ]]; then
	echo "❌ File not found: $LIST_FILE"
	exit 1
fi

echo "📦 Attempting to add packages from: $LIST_FILE (group: $GROUP)"
echo

while IFS= read -r package || [[ -n $package ]]; do
	pkg=$(echo "$package" | xargs) # trim whitespace
	if [[ -z $pkg ]]; then
		continue
	fi

	echo "➕ Trying to add: $pkg"
	if uv add --"$GROUP" "$pkg"; then
		echo "✅ Successfully added: $pkg"
	else
		echo "⚠️  Skipped (conflict): $pkg"
	fi
	echo
done <"$LIST_FILE"

echo "🎉 Done processing all packages."
