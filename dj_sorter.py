# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import csv
import re
import unicodedata

# The ultimate string cleaner: removes punctuation, accents, and spaces
def nuke_string(text):
    if not text: return ""
    text = unicodedata.normalize('NFKD', str(text)).encode('ascii', 'ignore').decode('ascii')
    return re.sub(r'[^a-z0-9]', '', text.lower())

def sort_rekordbox_fuzzy(xml_file, csv_file, output_file):
    print("Loading CSV and applying Fuzzy Logic cleaning...")
    csv_tracks = []
    
    try:
        with open(csv_file, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                raw_title = row.get('Track Title', '').strip()
                raw_artist = row.get('Artist', '').strip()
                crate = row.get('Crate', '').strip()
                if raw_title and crate:
                    csv_tracks.append({
                        'clean_title': nuke_string(raw_title),
                        'clean_artist': nuke_string(raw_artist),
                        'crate': crate
                    })
    except Exception:
        print("❌ Could not load data.csv")
        return

    print("Loading Rekordbox XML...")
    tree = ET.parse(xml_file)
    root = tree.getroot()
    collection = root.find('COLLECTION')
    playlists_root = root.find('.//PLAYLISTS/NODE')

    crates = {}
    matched = 0

    print("Matching tracks (Ignoring punctuation, spaces, and remix tags)...")
    for track in collection.findall('TRACK'):
        track_id = track.get('TrackID')
        xml_title = nuke_string(track.get('Name', ''))
        xml_artist = nuke_string(track.get('Artist', ''))
        
        target_crate = None
        
        # 1. Try Exact Clean Match
        for ct in csv_tracks:
            if ct['clean_title'] == xml_title and ct['clean_artist'] == xml_artist:
                target_crate = ct['crate']
                break
        
        # 2. Try Partial/Fuzzy Match (e.g. "Track Name" matches "Track Name (Original Mix)")
        if not target_crate:
            for ct in csv_tracks:
                if len(ct['clean_title']) > 3 and (ct['clean_title'] in xml_title or xml_title in ct['clean_title']):
                    if (ct['clean_artist'] in xml_artist or xml_artist in ct['clean_artist'] or not ct['clean_artist']):
                        target_crate = ct['crate']
                        break

        if target_crate:
            matched += 1
            if target_crate not in crates:
                crates[target_crate] = []
            crates[target_crate].append(track_id)

    print(f"\n🎉 Success! Fuzzy Logic matched {matched} tracks.")
        
    if matched > 0:
        print(f"Building {len(crates)} new crates...")
        auto_folder = ET.SubElement(playlists_root, 'NODE')
        auto_folder.set('Name', 'Excel Imported Crates')
        auto_folder.set('Type', '0')
        auto_folder.set('Count', str(len(crates)))

        for crate_name, track_ids in sorted(crates.items()):
            node = ET.SubElement(auto_folder, 'NODE')
            node.set('Name', crate_name)
            node.set('Type', '1')
            node.set('KeyType', '0')
            node.set('Entries', str(len(track_ids)))
            for tid in track_ids:
                ET.SubElement(node, 'TRACK').set('Key', tid)

        tree.write(output_file, encoding='UTF-8', xml_declaration=True)
        print(f"✅ Done! Import '{output_file}' into Rekordbox.")

if __name__ == "__main__":
    sort_rekordbox_fuzzy("rekordbox.xml", "data.csv", "rekordbox_sorted.xml")