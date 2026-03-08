import json
import time
import os

# TODO: Add functionality for editing characters
# TODO: Add CUD microservice AND/OR Filter microservice
# TODO: Add Image Retrieval microservice

# Testing again to make sure nothing broke.

# def save_stories(stories)

# def load_stories()

def view_character(character):
    print(f"\n{character["name"]} ({character.get("role")})\n"
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

    timeout = 5
    start = time.time()
    while not os.path.exists(response_path):
        if time.time() - start > timeout:
            print("TIMEOUT: No response received")
        time.sleep(0.1)

    with open(response_path, "r") as f:
        response = json.load(f)

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


title = convert_title_to_ascii("Narrative Organizer")
commands = """mkstory - make a new story container
editstory - edit the title of the story container
delstory - delete a story container
viewstories - lists all story containers

mkchar - make a new character
delchar - delete a character
viewchar - view the details of one character
viewallchars - view all characters in a story

help - list commands
exit - end the program"""
running = True
story_containers = []

print(title)
print("-----------------------\n"
      "Hello and welcome to the Narrative Organizer!\n"
      "Type in one of the following commands to start organizing\n"
      "your characters using story containers.\n\n" + commands)

while running:
    user_command = input("\n> ").lower()

    if user_command == "mkstory":
        title = input("What would you like the story to be called: ")

        index = locate_story(story_containers, title)

        if index > -1:
            print(f"\n\"{title}\" already has a story container!")
        else:
            story_containers.append({"title": title, "characters": []})
            story_containers = sort_stories(story_containers)

            print(f"\nSuccessfully created a story container for \"{title}\"!")


    elif user_command == "editstory":
        old_title = input("Which story would you like to edit: ")

        index = locate_story(story_containers, old_title)

        if index > -1:
            new_title = input("\nWhat would you like the story to be called: ")

            story_containers[index].update({"title": new_title})
            story_containers = sort_stories(story_containers)

            print(f"\n\"{old_title}\" has been renamed to \"{new_title}\"")
        else:
            print(f"\nThe story container for \"{old_title}\" does not exist!")

    elif user_command == "delstory":
        title = input("Which story would you like to delete: ")

        index = locate_story(story_containers, title)

        if index > -1:
            print("\nWARNING: Deleting a story container also deletes all of its characters!")

            while True:
                confirmation = input(f"\nAre you sure you want to delete \"{title}\" (Y/N): ").lower()

                if confirmation == "y":
                    del story_containers[index]

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
        if len(story_containers) == 0:
            print("You haven't made any story containers!")
        else:
            for story in story_containers:
                print(story.get("title"))

    elif user_command == "mkchar":
        title = input("Which story does this character belong to: ")

        story_index = locate_story(story_containers, title)

        if story_index > -1:
            print("\nPlease fill in the following fields.\n")
            name = input("Name: ")

            char_index = locate_character(story_containers[story_index]["characters"], name)

            if char_index == -1:
                role = input("Role: ")
                gender = input("Gender: ")
                age = input("Age: ")
                species = input("Species: ")
                personality = input("Personality: ")
                appearance = input("Appearance: ")
                abilities = input("Abilities: ")

                story_containers[story_index].get("characters").append({
                    "name": name,
                    "role": role,
                    "gender": gender,
                    "age": age,
                    "species": species,
                    "personality": personality,
                    "appearance": appearance,
                    "abilities": abilities})

                story_containers[story_index].update({"characters":
                                                          sort_characters(
                                                              story_containers[
                                                                  story_index].get(
                                                                  "characters"))})

                print(f"\nSuccessfully added \"{name}\" to \"{title}\"!")

            else:
                print(f"\nYou already have a character in \"{title}\" named \"{name}\"!")

        else:
            print(f"\nThe story container for \"{title}\" does not exist!")

    elif user_command == "delchar":
        title = input("Which story does this character belong to: ")

        story_index = locate_story(story_containers, title)

        if story_index > -1:
            name = input("\nWhich character would you like to delete: ")

            char_index = locate_character(
                story_containers[story_index].get("characters"), name)

            if char_index > -1:
                while True:
                    confirmation = input(f"\nAre you sure you want to delete \"{name}\" (Y/N): ").lower()

                    if confirmation == "y":
                        del story_containers[story_index].get("characters")[char_index]

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

        story_index = locate_story(story_containers, title)

        if story_index > -1:
            if view_all_characters(story_containers[story_index]):
                story_characters = story_containers[story_index].get(
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

        index = locate_story(story_containers, title)

        if index > -1:
            view_all_characters(story_containers[index])
        else:
            print(f"\nThe story container for \"{title}\" does not exist!")

    elif user_command == "help":
        print(commands)

    elif user_command == "exit":
        print("Thanks for using the Narrative Organizer!")
        running = False

    else:
        print("Invalid command.")