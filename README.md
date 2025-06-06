# Brave Filter List Generator

This project provides a simple tool to build a unified filter list
optimised for Brave's ad blocker. It fetches popular ad‑blocking lists,
processes them and generates a combined list with a standard header.

## Usage

```bash
python -m brave_filter --output brave_list.txt
```

The resulting `brave_list.txt` begins with the header:

```
! Title: Rody's Brave List
! Author: Murtaza Salih
! Version: <timestamp>
! Generated on: <iso date>
```

followed by the consolidated rules.
