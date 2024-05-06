import json
import sys

def load_json(filepath):
    with open(filepath) as file:
        return json.load(file)

def look(room):
    print(f"> {room['name']}\n\n{room['desc']}\n")
    if 'items' in room and room['items']:
        print('Items:', ', '.join(room['items'])+'\n')
    print('Exits:', ' '.join(room['exits'])+'\n' )

def go(rooms, current_room, direction):
    exits = rooms[current_room]['exits']
    if direction in exits:
        print(f"You go {direction}.\n")
        return exits[direction]
    else:
        print(f"There's no way to go {direction}.")
        return current_room

def get(rooms, current_room, item, inventory):
    if item:
        if 'items' in rooms[current_room]:
            if item in rooms[current_room]['items']:
                inventory.append(item)
                rooms[current_room]['items'].remove(item)
                print(f"You pick up the {item}.")
        else:
            print(f"There's no {item} anywhere.")
    else:
        print("Sorry, you need to 'get' something.")

def drop(rooms, current_room, item, inventory):
    if item:
        if item in inventory:
            inventory.remove(item)
            if 'items' in rooms[current_room]:
                rooms[current_room]['items'].append(item)
            else:
                rooms[current_room]['items'] = [item]
            print(f"You drop the {item}.")
        elif item not in inventory:
            print(f"You're not carrying {item}.")
        else:
            print(f"There's no {item} to drop in this room.")
    else:
        print("Sorry, you need to 'drop' something.")

def view_inventory(inventory):
    if not inventory:
        print("You're not carrying anything.")
    else:
        print("Inventory:")
        for item in inventory:
            print(f"  {item}")


def help():
    print("You can run the following commands:")
    print("  go ...")
    print("  get ...")
    print("  drop ...")
    print("  look")
    print("  inventory")
    print("  quit")
    print("  help")

def main(file):
    data = load_json(file)
    rooms_data = data['rooms']
    rooms = {room['name']: room for room in rooms_data}
    start_room_name = data['start']
    current_room = start_room_name
    inventory = []
    look(rooms[current_room])

    while True:
        try:
            action = input("What would you like to do? ").lower().strip()
        except EOFError:
            print("use 'quit' to exit.")
            continue

        if action == 'go':
            print("Sorry, you need to 'go' somewhere.")

        elif action.startswith('go '):
            direction = action.split(' ', 1)[-1]  
            temp = current_room
            current_room = go(rooms, current_room, direction)
            if temp == current_room:
                pass
            else:
                look(rooms[current_room])

        elif action == 'look':
            look(rooms[current_room])

        elif action.startswith('get '):
            if action[1]:
                item = action.split(' ', 1)[-1]
                get(rooms, current_room, item, inventory)
            else:
                print("You need to 'get' something.")

        elif action == 'get':
            print("Sorry, you need to 'get' something.")

        elif action == 'inventory':
            view_inventory(inventory)

        elif action == 'drop':
            print("Sorry, you need to 'drop' something.")

        elif action.startswith('drop '):
            item = action.split(' ', 1)[-1]
            drop(rooms, current_room, item, inventory)

        elif action == 'quit':
            print("Goodbye!")
            break

        elif action == 'help':
            help()
        
        elif action in ['n', 'e', 'w', 's', 'ne', 'nw' ,'se' ,'sw', 'north', 'south', 'west', 'east', 'northeast', 'northwest', 'southeast', 'southwest']:
            if action == 'n' or action == 'north':
                action = 'north'
            elif action == 'e' or action == 'east':
                action = 'east'
            elif action == 'w' or action == 'west':
                action = 'west'
            elif action == 's' or action == 'south':
                action = 'south'
            elif action == 'ne' or action == 'northeast':
                action = 'northeast'
            elif action == 'nw' or action == 'northwest':
                action = 'northwest'
            elif action == 'se' or action == 'southeast':
                action = 'southeast'
            elif action == 'sw' or action == 'southwest':
                action = 'southwest'
            temp = current_room
            current_room = go(rooms, current_room, action)
            if temp == current_room:
                pass
            else:
                look(rooms[current_room])

        else:
            print("Use 'quit' to exit.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Valid Usage: python/python3 script.py [map filename]")
        sys.exit(1)

    file = sys.argv[1]
    main(file)
