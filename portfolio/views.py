from sys import stdout
from django.shortcuts import render
from django.http import JsonResponse
import json, random
from django.views.decorators.csrf import csrf_exempt
from .models import (
    Command,
    Directory,
    File,
    Note,
    Neofetch,
)  # Your model for storing respons
from rest_framework.decorators import api_view

# Create your views here.


def index(request):
    return render(request, "portfolio/index.html")


@api_view(["POST"])
def htmx_term_res(request):
    context = {"stdout": "An Error has Occured!"}

    if request.method == "POST":
        command = request.data.get("command")

        pwd = request.data.get("pwd")

        dir_array = pwd.split("/")

        parent_directory = Directory.objects.filter(name=dir_array[-2] + "/").first()

        directories = Directory.objects.filter(parent_directory=parent_directory)

        args = request.POST.get("args")

        command_valid = Command.objects.filter(name=command).first()
        files = File.objects.filter(directory=parent_directory)

        if command_valid:
            if command_valid.name == "game":
                return render(request, "portfolio/games/highway-racer.html")

            if command_valid == "neofetch":
                art_db = Neofetch.objects.all()
                art_list = list(art_db)
                random_art = random.choice(art_list)

                context = {"cmd": command.name, "stdout": random_art.content}

            if not args and command_valid.name == "cat":
                context = {"response_obj": "No args supplied for cat."}

            if command_valid.name == "cat" and args:
                if files:
                    for file in files:
                        if args == file.title:
                            context = {
                                "cmd": command,
                                "pwd": pwd,
                                "stdout": file.content,
                            }
                            return render(
                                request, "portfolio/partials/markdown.html", context
                            )
            context = {"cmd": command, "stdout": command}
            return render(request, "portfolio/partials/markdown.html", context)
        else:
            context = {"stdout": "Command not found"}

        return render(request, "portfolio/partials/markdown.html", context)

    return render(request, "portfolio/partials/markdown.html", context)


@api_view(["POST"])
def execute_command(request):
    context = {"stdout": ""}

    # Get the command from the request body
    user_input = request.data.get("command")

    command = Command.objects.filter(name=user_input).first()
    pwd = request.data.get("pwd")
    args = request.data.get("args")
    print(command.name)
    if command:
        match command.name:
            case "ls":
                dir_array = pwd.split("/")

                parent_directory = Directory.objects.filter(
                    name=dir_array[-2] + "/"
                ).first()

                directories = Directory.objects.filter(
                    parent_directory=parent_directory
                )

                files = File.objects.filter(directory=parent_directory)

                file_list = list(files.values_list("title", flat=True))
                dir_list = list(directories.values_list("name", flat=True))
                dir_content = file_list + dir_list
                file_names = "\n\r".join([file.title for file in files])

                directory_names = "\n\r".join(
                    [directory.name for directory in directories]
                )
                context = {
                    "cmd": command.name,
                    "dir_content": dir_content,
                    "stdout": directory_names + "\n\r" + file_names,
                }
                return JsonResponse(context)

            case "id":
                context = {"cmd": command.name, "stdout": "shawnco"}

            case "neofetch":
                art_db = Neofetch.objects.all()
                art_list = list(art_db)
                random_art = random.choice(art_list)

                context = {"cmd": command.name, "stdout": random_art.content}

            case "?":
                man_page = (
                    "NAME\r\n"
                    "    basic-commands - Simple explanations for common shell commands\r\n"
                    "\r\n"
                    "SYNOPSIS\r\n"
                    "    ls      List directory contents\r\n"
                    "\r\n"
                    "    cat     Display the contents of a file\r\n"
                    "\r\n"
                    "    id      Show user and group IDs\r\n"
                    "\r\n"
                    "    cd      Change the current directory\r\n"
                    "\r\n"
                )
                context = {"cmd": command.name, "stdout": man_page}

            case "cd":
                context = {"cmd": command.name, "pwd": "/", "stdout": ""}

                dir_array = pwd.split("/")

                parent_directory = Directory.objects.filter(
                    name=dir_array[-2] + "/"
                ).first()

                directories = Directory.objects.filter(
                    parent_directory=parent_directory
                )

                if len(args) == 0:
                    return JsonResponse(context)

                if args[0] == "..":
                    dir_array = dir_array[:-2]

                    dir_string = "/".join(dir_array) + "/"
                    context = {
                        "cmd": command.name,
                        "pwd": dir_string,
                        "stdout": "",
                    }
                    return JsonResponse(context)

                if directories:
                    for directory in directories:
                        if args[0] + "/" == directory.name or args[0] == directory.name:
                            context = {
                                "cmd": command.name,
                                "pwd": pwd + directory.name,
                                "stdout": "",
                            }
                            return JsonResponse(context)

                return JsonResponse(context)

            case "cat":
                if len(args) == 0:
                    context = {"stderr": "No args supplied for cat."}
                    return JsonResponse(context)

                dir_array = pwd.split("/")

                parent_directory = Directory.objects.filter(
                    name=dir_array[-2] + "/"
                ).first()

                directories = Directory.objects.filter(
                    parent_directory=parent_directory
                )

                files = File.objects.filter(directory=parent_directory)

                file_names = "\n\r".join([file.title for file in files])

                directory_names = "\n\r".join(
                    [directory.name for directory in directories]
                )

                if directories:
                    for directory in directories:
                        if args[0] + "/" == directory.name or args[0] == directory.name:
                            context = {
                                "cmd": command.name,
                                "pwd": pwd,
                                "stdout": "This is a Directory",
                            }
                            return JsonResponse(context)

                if files:
                    for file in files:
                        if args[0] == file.title:
                            context = {
                                "cmd": command.name,
                                "pwd": pwd,
                                "stdout": file.content,
                            }
                            return JsonResponse(context)

                context = {"cmd": command.name, "stdout": directory_names + file_names}
                return JsonResponse(context)

    elif user_input != "":
        context = {"stderr": "Command not found"}

        return JsonResponse(context)

    return JsonResponse(context)
