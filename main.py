import json
import time
import os

# TODO: Add functionality for editing characters
# TODO: Add functionality for picking role rather than manually typing it

def view_character(character):
    print(f"\n{character.get("name")} ({character.get("role")})\n"
          f"_____________\n"
          f"Gender: {character.get("gender")}\n"
          f"Age: {character.get("age")}\n"
          f"Species: {character.get("species")}\n"
          f"Personality: {character.get("personality")}\n"
          f"Appearance: {character.get("appearance")}\n"
          f"Abilities: {character.get("abilities")}")


def view_all_characters(story):
    characters = story.get("characters")

    if len(characters) == 0:
        print(f"You haven't made any characters for \"{story.get("title")}\"!")
        return False
    else:
        for index in range(len(characters)):
            print(f"{index + 1}. {characters[index].get("name")} "
                  f"({characters[index].get("role")})")
        return True


def view_all_main_characters(story):
    request_path = "filter-request.json"
    response_path = "filter-response.json"

    characters = story.get("characters")

    filters = [{"field": "role", "op": "eq", "value": "Main Character"}]

    with open(request_path, "w") as f:
        json.dump({"data": characters, "filters": filters}, f)

    while True:
        try:
            with open(response_path, "r") as f:
                response = json.load(f)
                break
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.1)
            continue

    os.remove(response_path)
    main_characters = response.get("result", [])

    if len(main_characters) == 0:
        print(f"\n{story.get("title")} has no main characters!")
    else:
        for character in main_characters:
            view_character(character)


def locate_story(stories, title):
    for index in range(len(stories)):
        if stories[index].get("title") == title:
            return index
    return -1


def locate_character(characters, name):
    for index in range(len(characters)):
        if characters[index].get("name") == name:
            return index
    return -1


def convert_title_to_ascii(title):
    request_path = "title-request.json"
    response_path = "title-response.json"

    request_data = {"text": title}
    with open(request_path, "w") as f:
        json.dump(request_data, f)

    while True:
        try:
            with open(response_path, "r") as f:
                response = json.load(f)
                break
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.1)
            continue

    os.remove(response_path)
    return response.get("result")


def sort_stories(stories):
    request_path = "sort-request.json"
    response_path = "sort-response.json"

    request_data = {
        "sort_list": stories,
        "sort_property": "title",
        "sort_order": "ascending"
    }

    with open(request_path, "w") as f:
        json.dump(request_data, f)

    while True:
        try:
            with open(response_path, "r") as f:
                response = json.load(f)
                break
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.1)
            continue

    os.remove(response_path)
    return response.get("result")


def sort_characters(characters):
    request_path = "sort-request.json"
    response_path = "sort-response.json"

    request_data = {
        "sort_list": characters,
        "sort_property": "name",
        "sort_order": "ascending"
    }

    with open(request_path, "w") as f:
        json.dump(request_data, f, indent=4)

    while True:
        try:
            with open(response_path, "r") as f:
                response = json.load(f)
                break
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.1)
            continue

    os.remove(response_path)
    return response.get("result")


def store_reference(image_path, char_name):
    request_path = "image-request.json"
    response_path = "image-response.json"

    data = {
        "action": "store",
        "source_path": image_path,
        "name": f"{char_name}"
    }

    with open(request_path, "w") as f:
        json.dump(data, f, indent=4)

    while True:
        try:
            with open(response_path, "r") as f:
                response = json.load(f)
                break
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.1)
            continue

    os.remove(response_path)
    return response


def delete_reference(char_name):
    request_path = "image-request.json"
    response_path = "image-response.json"

    data = {
        "action": "delete",
        "name": f"{char_name}"
    }

    with open(request_path, "w") as f:
        json.dump(data, f, indent=4)

    while True:
        try:
            with open(response_path, "r") as f:
                response = json.load(f)
                break
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.1)
            continue

    os.remove(response_path)
    return response


def view_reference(char_name):
    request_path = "image-request.json"
    response_path = "image-response.json"

    data = {
        "action": "open",
        "name": f"{char_name}",
    }

    with open(request_path, "w") as f:
        json.dump(data, f, indent=4)

    while True:
        try:
            with open(response_path, "r") as f:
                response = json.load(f)
                break
        except (json.JSONDecodeError, FileNotFoundError):
            time.sleep(0.1)
            continue

    os.remove(response_path)
    return response


title = convert_title_to_ascii("Narrative Organizer")
commands = """mkstory - make a new story container
editstory - edit the title of the story container
delstory - delete a story container
viewstories - lists all story containers

mkchar - make a new character
delchar - delete a character
viewchar - view the details of one character
viewallchars - view all characters in a story
viewmainchars - view the details of all main characters in a story

mkref - add a character reference
delref - delete a character reference
viewref - view a character reference

help - list commands
exit - end the program"""
running = True
stories = []

print(title)
print("-----------------------\n"
      "Hello and welcome to the Narrative Organizer!\n"
      "Type in one of the following commands to start organizing\n"
      "your characters using story containers.\n\n" + commands)

while running:
    user_command = input("\n> ").lower()

    if user_command == "mkstory":
        title = input("What would you like the story to be called: ")

        index = locate_story(stories, title)

        if index > -1:
            print(f"\n\"{title}\" already has a story container!")
        else:
            stories.append({"title": title, "characters": []})
            stories = sort_stories(stories)

            print(f"\nSuccessfully created a story container for \"{title}\"!")

    elif user_command == "editstory":
        old_title = input("Which story would you like to edit: ")

        index = locate_story(stories, old_title)

        if index > -1:
            new_title = input("\nWhat would you like the story to be called: ")

            stories[index].update({"title": new_title})
            stories = sort_stories(stories)

            print(f"\n\"{old_title}\" has been renamed to \"{new_title}\"")
        else:
            print(f"\nThe story container for \"{old_title}\" does not exist!")

    elif user_command == "delstory":
        title = input("Which story would you like to delete: ")

        index = locate_story(stories, title)

        if index > -1:
            print("\nWARNING: Deleting a story container also deletes all of its characters!")

            while True:
                confirmation = input(f"\nAre you sure you want to delete \"{title}\" (Y/N): ").lower()

                if confirmation == "y":
                    del stories[index]

                    print(f"\nSuccessfully deleted \"{title}\"!")
                    break
                elif confirmation == "n":
                    print(f"\nCanceled deletion of \"{title}\".")
                    break
                else:
                    print("\nInvalid input")
        else:
            print(f"\nThe story container for \"{title}\" does not exist!")

    elif user_command == "viewstories":
        if len(stories) == 0:
            print("You haven't made any story containers!")
        else:
            for story in stories:
                print(story.get("title"))

    elif user_command == "mkchar":
        title = input("Which story does this character belong to: ")

        story_index = locate_story(stories, title)

        if story_index > -1:
            print("\nPlease fill in the following fields.\n")
            name = input("Name: ")

            char_index = locate_character(stories[story_index]["characters"], name)

            if char_index == -1:
                role = input("Role: ")
                gender = input("Gender: ")
                age = input("Age: ")
                species = input("Species: ")
                personality = input("Personality: ")
                appearance = input("Appearance: ")
                abilities = input("Abilities: ")

                stories[story_index].get("characters").append({
                    "name": name,
                    "role": role,
                    "gender": gender,
                    "age": age,
                    "species": species,
                    "personality": personality,
                    "appearance": appearance,
                    "abilities": abilities,
                    "reference": False})

                stories[story_index].update({"characters":
                                                          sort_characters(
                                                              stories[
                                                                  story_index].get(
                                                                  "characters"))})

                print(f"\nSuccessfully added \"{name}\" to \"{title}\"!")

            else:
                print(f"\nYou already have a character in \"{title}\" named \"{name}\"!")

        else:
            print(f"\nThe story container for \"{title}\" does not exist!")

    elif user_command == "delchar":
        title = input("Which story does this character belong to: ")

        story_index = locate_story(stories, title)

        if story_index > -1:
            name = input("\nWhich character would you like to delete: ")

            char_index = locate_character(
                stories[story_index].get("characters"), name)

            if char_index > -1:
                while True:
                    confirmation = input(f"\nAre you sure you want to delete \"{name}\" (Y/N): ").lower()

                    if confirmation == "y":
                        del stories[story_index].get("characters")[char_index]

                        has_reference = stories[story_index].get("characters")[
                            char_index].get("reference")

                        if has_reference:
                            delete_reference(name)
                            stories[story_index].get("characters")[
                                char_index].update(
                                {"reference": False})

                        print(f"\nSuccessfully deleted \"{name}\"!")
                        break
                    elif confirmation == "n":
                        print(f"\nCanceled deletion of \"{name}\".")
                        break
                    else:
                        print("\nInvalid input")

            else:
                print(f"\nThe character \"{name}\" does not exist in \"{title}\"!")

        else:
            print(f"\nThe story container for \"{title}\" does not exist!")

    elif user_command == "viewchar":
        title = input("Which story does this character belong to: ")

        story_index = locate_story(stories, title)

        if story_index > -1:
            if view_all_characters(stories[story_index]):
                story_characters = stories[story_index].get(
                    "characters")

                character = input("\nWhich character would you like to view ("
                             "enter character name or corresponding number): ")

                try:
                    char_index = int(character) - 1

                    if 0 <= char_index < len(story_characters):
                        view_character(story_characters[char_index])
                    else:
                        print("You entered a value out of range!")

                except ValueError:
                    char_index = locate_character(story_characters, character)

                    if char_index > -1:
                        view_character(story_characters[char_index])

                    else:
                        print(
                            f"\nThe character \"{character}\" does not exist in \"{title}\"!")

        else:
            print(f"\nThe story container for \"{title}\" does not exist!")

    elif user_command == "viewallchars":
        title = input("Which story would you like to view the characters of: ")

        index = locate_story(stories, title)

        if index > -1:
            view_all_characters(stories[index])
        else:
            print(f"\nThe story container for \"{title}\" does not exist!")

    elif user_command == "viewmainchars":
        title = input("Which story would you like to view the main characters of: ")

        index = locate_story(stories, title)

        if index > -1:
            view_all_main_characters(stories[index])
        else:
            print(f"\nThe story container for \"{title}\" does not exist!")

    elif user_command == "mkref":
        title = input("Which story does this character belong to: ")

        story_index = locate_story(stories, title)

        if story_index > -1:
            name = input("\nWhich character would you like to give a reference: ")

            char_index = locate_character(
                stories[story_index].get("characters"), name)

            if char_index > -1:
                has_reference = stories[story_index].get("characters")[char_index].get("reference")

                if not has_reference:
                    image_path = input("\nWhat is the path to the reference: ")

                    if os.path.exists(image_path):
                        store_reference(image_path, name)
                        stories[story_index].get("characters")[char_index].update(
                            {"reference": True})
                        print(f"\nSuccessfully gave \"{name}\" a reference!")
                    else:
                        print(f"\nInvalid path.")

                else:
                    print(f"\nThe character \"{name}\" already has a reference!")

            else:
                print(f"\nThe character \"{name}\" does not exist in \"{title}\"!")

        else:
            print(f"\nThe story container for \"{title}\" does not exist!")

    elif user_command == "delref":
        title = input("Which story does this character belong to: ")

        story_index = locate_story(stories, title)

        if story_index > -1:
            name = input("\nWhich character would you like to delete the reference of: ")

            char_index = locate_character(
                stories[story_index].get("characters"), name)

            if char_index > -1:
                has_reference = stories[story_index].get("characters")[
                    char_index].get("reference")

                if has_reference:
                    delete_reference(name)
                    stories[story_index].get("characters")[char_index].update(
                        {"reference": False})
                    print(f"\nSuccessfully deleted the reference for \"{name}\"!")
                else:
                    print(f"\nThe character \"{name}\" doesn't have a reference!")

            else:
                print(
                    f"\nThe character \"{name}\" does not exist in \"{title}\"!")

        else:
            print(f"\nThe story container for \"{title}\" does not exist!")

    elif user_command == "viewref":
        title = input("Which story does this character belong to: ")

        story_index = locate_story(stories, title)

        if story_index > -1:
            name = input("\nWhich character would you like to view the reference of: ")

            char_index = locate_character(
                stories[story_index].get("characters"), name)

            if char_index > -1:
                has_reference = stories[story_index].get("characters")[
                    char_index].get("reference")

                if has_reference:
                    view_reference(name)
                else:
                    print(f"\nThe character \"{name}\" doesn't have a reference!")

            else:
                print(
                    f"\nThe character \"{name}\" does not exist in \"{title}\"!")

        else:
            print(f"\nThe story container for \"{title}\" does not exist!")

    elif user_command == "help":
        print(commands)

    elif user_command == "exit":
        print("Thanks for using the Narrative Organizer!")
        running = False

    else:
        print("Invalid command.")