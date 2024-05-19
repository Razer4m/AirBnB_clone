#!/usr/bin/python3
import cmd
import re
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """Command interpreter for HBNB"""
    prompt = "(hbnb) "

    classes = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        return True

    def emptyline(self):
        """Do nothing on empty input line"""
        pass

    def do_create(self, arg):
        """
        Creates a new instance of BaseModel,
        saves it (to the JSON file) and prints the id
        """
        if not arg:
            print("** class name missing **")
            return
        if arg not in self.classes:
            print("** class doesn't exist **")
            return
        new_instance = self.classes[arg]()
        new_instance.save()
        print(new_instance.id)

    def do_show(self, arg):
        """
        Prints the string representation of
        an instance based on the class name and id
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        print(storage.all()[key])

    def do_destroy(self, arg):
        """Deletes an instance on the class name and id"""
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return
        del storage.all()[key]
        storage.save()

    def do_all(self, arg):
        """
        Prints all string representation of
        all instances based or not on the class name
        """
        if arg and arg not in self.classes:
            print("** class doesn't exist **")
            return
        objects = storage.all()
        result = []
        for obj in objects.values():
            if not arg or obj.__class__.__name__ == arg:
                result.append(str(obj))
        print(result)

    def do_update(self, arg):
        """
        Updates an instance based on the class
        name and id by adding or updating attribute
        """
        args = arg.split(maxsplit=3)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in self.classes:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return

        key = f"{args[0]}.{args[1]}"
        if key not in storage.all():
            print("** no instance found **")
            return

        obj = storage.all()[key]

        if len(args) == 3:
            # Handle dictionary update
            try:
                updates = json.loads(args[2])
                if not isinstance(updates, dict):
                    raise ValueError()
                for attr_name, attr_value in updates.items():
                    if hasattr(obj, attr_name):
                        attr_type = type(getattr(obj, attr_name))
                        setattr(obj, attr_name, attr_type(attr_value))
                    else:
                        setattr(obj, attr_name, attr_value)
                obj.save()
            except json.JSONDecodeError:
                print("** invalid dictionary **")
            except ValueError:
                print("** attribute value error **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return
        if len(args) < 4:
            print("** value missing **")
            return

        attr_name = args[2]
        attr_value = args[3]

        try:
            # Convert the attribute value to the correct type
            if hasattr(obj, attr_name):
                attr_type = type(getattr(obj, attr_name))
                setattr(obj, attr_name, attr_type(attr_value))
            else:
                setattr(obj, attr_name, attr_value)
            obj.save()
        except Exception as e:
            print(f"** error updating attribute: {e} **")

    def do_count(self, arg):
        """Retrieve the number of instances of a class"""
        if not arg:
            print("** class name missing **")
            return
        if arg not in self.classes:
            print("** class doesn't exist **")
            return
        count = sum(
            1 for obj in storage.all().values()
            if obj.__class__.__name__ == arg
        )
        print(count)

    def default(self, line):
        """Handle default cases for custom commands"""
        match_all = re.fullmatch(r"(\w+)\.all\(\)", line)
        if match_all:
            class_name = match_all.group(1)
            if class_name in self.classes:
                self.do_all(class_name)
            else:
                print("** class doesn't exist **")
            return

        match_count = re.fullmatch(r"(\w+)\.count\(\)", line)
        if match_count:
            class_name = match_count.group(1)
            if class_name in self.classes:
                self.do_count(class_name)
            else:
                print("** class doesn't exist **")
            return

        match_show = re.fullmatch(r"(\w+)\.show\((.+)\)", line)
        if match_show:
            class_name = match_show.group(1)
            instance_id = match_show.group(2).strip('"')
            if class_name in self.classes:
                self.do_show(f"{class_name} {instance_id}")
            else:
                print("** class doesn't exist **")
            return

        match_destroy = re.fullmatch(r"(\w+)\.destroy\((.+)\)", line)
        if match_destroy:
            class_name = match_destroy.group(1)
            instance_id = match_destroy.group(2).strip('"')
            if class_name in self.classes:
                self.do_destroy(f"{class_name} {instance_id}")
            else:
                print("** class doesn't exist **")
            return

        match_update_dict = re.fullmatch(
            r'(\w+)\.update\((.+), (.+)\)', line
        )
        if match_update_dict:
            class_name = match_update_dict.group(1)
            instance_id = match_update_dict.group(2).strip('"')
            updates = match_update_dict.group(3)
            if class_name in self.classes:
                self.do_update(f'{class_name} {instance_id} {updates}')
            else:
                print("** class doesn't exist **")
            return

        match_update = re.fullmatch(
            r'(\w+)\.update\((.+), (.+), (.+)\)', line
        )
        if match_update:
            class_name = match_update.group(1)
            instance_id = match_update.group(2).strip('"')
            attr_name = match_update.group(3).strip('"')
            attr_value = match_update.group(4).strip('"')
            if class_name in self.classes:
                self.do_update(
                    f'{class_name} {instance_id} {attr_name} {attr_value}'
                )
            else:
                print("** class doesn't exist **")
            return

        print(f"*** Unknown syntax: {line}")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
