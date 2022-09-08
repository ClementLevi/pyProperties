# -*- coding: utf-8 -*-
# @Author:Clement_Levi
# @Contact: 1090708360@qq.com
# @MIT License

# Copyright (c) 2022 Clement Levi
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class Properties:
    """Java style *.properties manager class. Can read from a *.properties file and display in dictionary.
    """

    # While coding, referred to https://blog.csdn.net/Cameron_Rin/article/details/120789880
    def __init__(self, file_name: str):
        """One instance must be bound with a existing file.
        Data is stored in a  structure like:
                    --------------------------------
        _isComment | 1 |  0  | 1 |  0  |  0  |  0  | ...
        properties | # | K:V | # | K:V | K:V | K:V | ...
                    --------------------------------
        The index of this array shows the line number they originally were.
        """
        self.fileName = file_name
        self._isComment: list[int] = []
        self.properties: list[str | dict] = []

        self.fread()

    def fread(self, file_name: str = '') -> list:
        """Read possible configurations from a *.properties file. Note that if not manually called,
        a file will be read only once when creating an instance.
        TODO: Make in-line comment recognizable.
        TODO: Keep empty line format after rewriting a file.
        :param file_name: optional, should be a URL of *.properties file.
                If left blank, the value will be the used one when this instance created.
        """
        if not file_name:
            file_name = self.fileName
        with open(file_name, 'r', encoding="utf-8") as pro_file:
            try:
                # Read *.properties file by line

                for line in pro_file:
                    # Save comments by identifying "#..."
                    # ! Not support in-line comment yet: "key=value   # comment..."
                    if line.find('#') == 0:
                        self.properties.append(line.replace('#', '').replace('\n', ''))
                        self._isComment.append(1)

                    # Save config items by identifying "="
                    elif line.find('=') > 0:
                        config = line.replace('\n', '').split('=')
                        self.properties.append({config[0]: config[1]})
                        self._isComment.append(0)

                    # Empty line or invalid line
                    else:
                        pass
            except Exception as e:
                raise e
        return self.properties

    def fwrite(self) -> None:
        """Overwrite the configurations into the file. The modification should have
        been saved in an instance.
        """
        buffer: list[str | dict] = []
        for data_num in range(len(self.properties)):
            if self._isComment[data_num]:
                # Write in comment directly
                buffer.append('# ' + self.properties[data_num] + '\n')
            else:
                # Unpack the dict and formulate into config template
                key, value = self.properties[data_num].popitem()
                buffer.append("%s=%s\n" % (key, value))
        # Remove last \n of the file
        buffer[-1].rstrip()

        try:
            with open(self.fileName, 'w', encoding="utf-8") as pro_file:
                pro_file.writelines(buffer)
        except Exception as e:
            raise e
        return None

    def get_all_properties(self) -> dict:
        """Get all property items as a dictionary in Python. Note that
        conflicting items will be overwritten by latter ones.
        :return: all property items as a dictionary."""
        all_properties = {}
        for data_num in range(len(self.properties)):
            # Filter all config items out
            if not self._isComment[data_num]:
                all_properties.update(self.properties[data_num])
        return all_properties

    def get_property(self, arg: str) -> str:
        """Call ~.get_all_properties() to look up for specific item.
        Not faster but easier to understand, I think.
        :param arg: the property name user want to access.
        :return: specified property value."""
        for data_num in range(len(self.properties)):
            if not self._isComment[data_num]:
                if arg in self.properties[data_num].keys():
                    return self.properties[data_num][arg]
        raise IndexError("No configuration item names '%s'." % arg)

    def set_property(self, *kv) -> int:
        """ Receive multiple dictionaries to set configurations.
        TODO: make it possible to receive one dict with multiple k-v sets
        :return: how many properties are set."""
        for arg in kv:
            # Check if input is a dict
            if not isinstance(arg, dict):
                # Not dict input
                raise TypeError("Wrong argument: expecting 'dict', while received '%s'." % type(arg))
            else:
                # Handle the input argument
                # Search for existing configuration item
                for data_num in range(len(self.properties)):
                    if not self._isComment[data_num]:
                        if list(arg)[0] in self.properties[data_num].keys():
                            self.properties[data_num].update(arg)
                            break
                # No existing item. Create a new configuration item
                else:
                    self.properties.append(arg)
                    self._isComment.append(0)
        return len(kv)

    def __str__(self):
        return str(self.get_all_properties())


if __name__ == "__main__":
    # Example usage
    P = Properties("example.properties")

    print(P.get_all_properties())

    P.set_property({"new-item": 1919810}, {"try-change-this": 0})
    print(P.get_all_properties())

    P.fwrite()
    print(P.get_all_properties())
