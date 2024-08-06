import re
import string

from hstest import StageTest, CheckResult, dynamic_test, TestedProgram


class Feedback:
    contain_msg = "Your output should contain the decoded message."
    file_not_found_msg = "File secret-message.txt not found."
    read_end_msg = "After reading the file, your output should contain the message: "


class MessageDecipherTest(StageTest):
    decode_end_msg = "Finished decoding the file"
    secret_message_path = "secret-message.txt"
    letters = list(string.ascii_lowercase)
    reversed_letters = letters[::-1]

    @classmethod
    def read_file(cls, path):
        try:
            with open(path, "r") as file:
                return file.read().strip()
        except FileNotFoundError:
            return False

    @classmethod
    def replacer(cls, char):
        i = cls.reversed_letters.index(char.lower())
        replaced_char = cls.letters[i]
        return replaced_char.upper() if char.isupper() else replaced_char

    @classmethod
    def decode_message(cls):
        chunk = cls.read_file(cls.secret_message_path)
        if not chunk:
            return False

        output = re.sub(r'[a-zA-Z]', lambda x: cls.replacer(x.group()), chunk)
        return output

    @dynamic_test
    def test1(self):
        main = TestedProgram(self.source_name)
        file_output = self.decode_message()
        output = main.start()

        # test if the file exists
        if not file_output:
            return CheckResult.wrong(Feedback.file_not_found_msg + f" {self.secret_message_path}")

        # test if the output is correct
        if file_output.strip() not in output.strip():
            return CheckResult.wrong(Feedback.contain_msg)

        # test if the message is correct
        if self.decode_end_msg not in output.strip():
            return CheckResult.wrong(Feedback.read_end_msg + f" '{self.decode_end_msg}'")

        return CheckResult.correct()


if __name__ == '__main__':
    MessageDecipherTest('task').run_tests()
