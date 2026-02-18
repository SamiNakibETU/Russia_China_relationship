"""Analyze the truncated notebook to understand its structure."""
import re
import json

NB_PATH = r"d:\Users\Proprietaire\Desktop\Projet_perso\Chine-russie\notebooks\02_time_series_econometrics.ipynb"

with open(NB_PATH, "r", encoding="utf-8") as f:
    content = f.read()

print(f"File length: {len(content)} chars")

# Find all cell_type markers
cell_starts = [m.start() for m in re.finditer(r'"cell_type"', content)]
print(f"Cell type markers found: {len(cell_starts)}")

# Find source blocks
source_blocks = [m.start() for m in re.finditer(r'"source":\s*\[', content)]
print(f"Source blocks found: {len(source_blocks)}")

# Try to find how many cells are complete by looking for closing patterns
# Each cell in a notebook ends with a closing }
# Let's find the positions of each cell
for i, pos in enumerate(cell_starts):
    # Extract cell_type value
    ct_match = re.search(r'"cell_type":\s*"(\w+)"', content[pos:pos+50])
    ct = ct_match.group(1) if ct_match else "?"
    print(f"  Cell {i}: type={ct}, starts at char {pos}")

# Try to parse progressively
print("\n--- Attempting recovery ---")
# Find the last point where we can close valid JSON
# Look for the last complete "source" array close
last_good = 0
for m in re.finditer(r'\}\s*,?\s*\{', content):
    # This might be a cell boundary
    pass

# Try to find the last cell that has complete source
for i, sb_pos in enumerate(source_blocks):
    # Find the end of this source array
    bracket_depth = 0
    in_string = False
    escape = False
    pos = sb_pos + content[sb_pos:].index('[')
    for j in range(pos, min(pos + 500000, len(content))):
        c = content[j]
        if escape:
            escape = False
            continue
        if c == '\\':
            escape = True
            continue
        if c == '"' and not escape:
            in_string = not in_string
            continue
        if in_string:
            continue
        if c == '[':
            bracket_depth += 1
        elif c == ']':
            bracket_depth -= 1
            if bracket_depth == 0:
                last_good = j
                print(f"  Source block {i}: complete (ends at char {j})")
                break
    else:
        print(f"  Source block {i}: INCOMPLETE (truncated)")

# Find plt.show and figsize in source content
print("\n--- Content search ---")
show_matches = list(re.finditer(r'plt\.show\(\)', content))
print(f"plt.show() occurrences: {len(show_matches)}")

figsize_matches = list(re.finditer(r'figsize=\([^)]+\)', content))
print(f"figsize=(...) occurrences: {len(figsize_matches)}")
for m in figsize_matches:
    print(f"  {m.group()} at char {m.start()}")

dpi_matches = list(re.finditer(r'figure\.dpi', content))
print(f"figure.dpi occurrences: {len(dpi_matches)}")

savefig_matches = list(re.finditer(r'savefig\.dpi', content))
print(f"savefig.dpi occurrences: {len(savefig_matches)}")

figfigsize_matches = list(re.finditer(r'figure\.figsize', content))
print(f"figure.figsize occurrences: {len(figfigsize_matches)}")

gc_matches = list(re.finditer(r'import gc', content))
print(f"import gc occurrences: {len(gc_matches)}")
