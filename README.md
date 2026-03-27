# Rekordbox-AI-Sorter
This tool uses a Python script to match a Claude-categorized CSV to your library using fuzzy logic. It automatically builds energy-based crates via XML import, rescuing DJs from the "one big playlist" struggle.

I never coded a single line in my life. But I had this issue where my entire library was just one massive, unorganized playlist, and I couldn't decide what to play next. I built this with Claude Ai & Gemini to help me get a foundation started. I don't know who else needs this, but here it is.

Why I Made This

I was dealing with major "analysis paralysis." Staring at thousands of tracks in one folder while trying to mix is a nightmare. This isn't a "robot DJ"—it doesn't replace your ears. It just helps anyone who has their music in a single "dumping ground" finally build some "shelves" so they can actually find their tracks. It categorizes your library into whatever crates you want, so you can focus on the set, not the scrolling. Great for beginners or if you're absolute cheeks like me organizing things.

How It Works
1. The Analysis (Claude.ai)

Use AI to act as a librarian and sort your messy list.

    Export your Rekordbox collection as a CSV.

    Upload it to Claude.ai and say:

        "I have a massive, unorganized music library. Analyze this CSV and categorize these tracks into crates based on their energy, mood, and genre. You decide the crate names (e.g., Warmup, Peak, Melodic, etc.). Output a table with these headers: Track Title, Artist, and Crate."

    Save that table as data.csv on your desktop.

2. The Sync (The Python Script)

This script is the bridge. It takes that AI list and physically builds the folders in Rekordbox. It uses Fuzzy Logic, so it’s smart enough to match tracks even if the names are slightly different (like having "Original Mix" or extra punctuation in the title).

    Export your Rekordbox Collection as XML (rekordbox.xml) to your desktop.

    Run the script: python dj_sorter.py.

    In Rekordbox, go to the XML tab, hit Refresh, and Import the "AI Sorted Crates" folder.
