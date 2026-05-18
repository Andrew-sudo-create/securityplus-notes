# Security+ Notes

A structured Security+ study repository with timed, incremental publishing.

## Purpose

This repository is designed to document ongoing Security+ learning in a consistent, trackable format.  
Instead of publishing all notes at once, content is released gradually to reflect steady daily progress.

## How It Works

- Study notes are prepared in `.hidden-notes/`
- Published notes live in `notes/`
- Automation releases one note file per day from hidden to published notes
- The release is committed automatically to keep a daily contribution rhythm

## Content Organization

Notes are grouped by topic folders, with numbered files inside each folder for clear sequence.

Example:

```text
.hidden-notes/
`-- network-security/
    |-- 001-firewalls.md
    |-- 002-ids-ips.md
    `-- 003-vpns.md
```

Each day, the next eligible numbered note is moved to:

```text
notes/network-security/
```

## Publishing Model

The release process publishes one file at a time, preserving folder structure in `notes/`.  
This creates a clean timeline of learning progress and keeps the public notes archive organized by topic.

## Privacy Note

`.hidden-notes` is hidden by naming convention only.  
If this repository is public, unreleased notes in that folder are still visible.