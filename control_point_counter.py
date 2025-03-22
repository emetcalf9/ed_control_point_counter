import sys
import json

if len(sys.argv) > 1:
    filename = sys.argv[1]
else:
    filename = './example/Journal.log'
system_merits = {}
system_name = 'Uninitialized'
jump_count = 0
accumulated_merits = 0
merit_event_count = 0
with open(filename, 'r') as journal:
    for line in journal:
        entry = json.loads(line)
        if entry['event'] == 'Location':
          system_name = entry['StarSystem']
        elif entry['event'] == 'FSDJump':
            if entry['StarSystem'] in system_merits.keys():
                system_merits[system_name] += accumulated_merits
            else:
                system_merits[system_name] = accumulated_merits
            system_name = entry['StarSystem']
            accumulated_merits = 0
            jump_count += 1
        elif entry['event'] == 'PowerplayMerits':
            accumulated_merits += int(entry['MeritsGained'])
            merit_event_count += 1
if system_name in system_merits.keys():
    system_merits[system_name] += accumulated_merits
else:
    system_merits[system_name] = accumulated_merits
for key, value in system_merits.items():
    if value != 0:
        print(f"Merits:         {key}: {value}")
        print(f"Control Points: {key}: {int(value/4)}")
print('Jump Count: ' + str(jump_count))
print('Merit Event Count: ' + str(merit_event_count))
